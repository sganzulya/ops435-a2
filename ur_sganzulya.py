#!/usr/bin/env python3


  # authorship declaration

  # __author__ Steve Ganzulya
  # __date__ November 2019
  # __version__ 1.0 

import os 
import sys
import time
import argparse


def get_login_rec():
    login_rec = os.popen('last -Fiw').readlines()
    login_rec = [line.strip('\n') for line in login_rec]
    login_rec = login_rec[:-2] 
    login_rec = [record.strip('\n') for record in login_rec if len(record.split()) >= 15 and len(record.split()) <= 16]
    
    return login_rec
 
def read_login_rec(filelist):
    login_rec = []
    for filename in filelist: 
        if filename == ("last" or "Last"):
            login_rec +=get_login_rec()
        else:
            f = open(filename, 'r')
            login_rec.extend(list(f))
            f.close()
    login_rec = [line.strip('\n') for line in login_rec]
    if args.list: 
        string = "User" if args.list == 'user' else "Host"
        string += " list for"
        for filename in args.files:
            string += " " + filename
          
        string += "\n" + ("=" * len(string))
        print(string)
        stringList = []
        if args.list == 'user':
            for item in login_rec: 
                user = item.split()[0]
                if user not in stringList:
                    stringList.append(user)
                    print(user) 
        else:
            for item in login_rec:
                host = item.split()[2]
                if host not in stringList:
                    stringList.append(host)
                    print(host)
    
    
    return login_rec

def cal_daily_usage(subject,login_recs):
    dateUsage = {}
    total = 0
    print("Total", " ", " ", " ", "", "Usage in Seconds")
    for line in login_recs:
        line = line.split() 
        if line[0] == subject or line[2] == subject:
            normalizedRecords = normalized_rec(line)
            for normalizedRecord in normalizedRecords:
                loginDT = time.strptime(' '.join(normalizedRecord[4:8]), "%b %d %H:%M:%S %Y")
                logoutDT = time.strptime(' '.join(normalizedRecord[10:14]), "%b %d %H:%M:%S %Y")
                
                seconds = time.mktime(logoutDT) - time.mktime(loginDT)
                
                day = time.strftime("%Y/%m/%d", loginDT)
                if day not in dateUsage.keys():
                    dateUsage[day] = seconds
                else:
                    dateUsage[day] += seconds
                total += seconds
            
    [print(key, " ", round(value)) for key, value in dateUsage.items()]
    print("Total", " ", " ", " ", "", round(total))

def cal_weekly_usage(subject,login_recs):
    dateUsage = {}
    total = 0
    print("Total", " ", " ", " ", "", "Usage in Seconds")
    for line in login_recs:
        line = line.split() 
        if line[0] == subject or line[2] == subject:
            normalizedRecords = normalized_rec(line)
            for normalizedRecord in normalizedRecords:
                loginDT = time.strptime(' '.join(normalizedRecord[4:8]), "%b %d %H:%M:%S %Y")
                logoutDT = time.strptime(' '.join(normalizedRecord[10:14]), "%b %d %H:%M:%S %Y")
                
                seconds = time.mktime(logoutDT) - time.mktime(loginDT)
                week = time.strftime("%Y", loginDT) + "/" + str(round((loginDT.tm_yday - loginDT.tm_wday)/7 + 1))+ "\t  "
                if week not in dateUsage.keys():
                    dateUsage[week] = seconds
                else:
                    dateUsage[week] += seconds
                total += seconds
            
    [print(key, " ", round(value)) for key, value in dateUsage.items()]
    print("Total", "\t    ", round(total))
     
def normalized_rec(rec):
    jday = time.strftime('%j',time.strptime(' '.join(rec[4:6]+rec[7:8]),'%b %d %Y'))
    jday2 = time.strftime('%j',time.strptime(' '.join(rec[10:12]+rec[13:14]), '%b %d %Y'))
    if jday == jday2:
       norm_rec = []
       norm_rec.append(rec.copy())
       return norm_rec
    else:
       new_rec1 = rec.copy()
       new_rec = rec.copy()
       t_next = time.mktime(time.strptime(' '.join(new_rec1[4:6]+rec[7:8]),'%b %d %Y'))+86400
       next_day = time.strftime('%a %b %d %H:%M:%S %Y',time.strptime(time.ctime(t_next))).split()
       new_rec1[12] = '23:59:60'
       new_rec1[9] = new_rec1[3]
       new_rec1[10] = new_rec1[4]
       new_rec1[11] = new_rec1[5]
       new_rec[3] = next_day[0] 
       new_rec[4] = next_day[1] 
       new_rec[5] = next_day[2] 
       new_rec[6] = next_day[3] 
       new_rec[7] = next_day[4] 
       norm_rec = normalized_rec(new_rec)
       normalized_recs = norm_rec.copy()
       normalized_recs.insert(0,new_rec1)
    return normalized_recs 
      
if __name__ == '__main__':  
    parser = argparse.ArgumentParser(description="Usage Report based on the last command",epilog="Copyright 2018 - Steve Ganzulya")
    parser.add_argument("-l", "--list", type=str, choices=['user','host'], help="generate user name or remote host IP from the given files")
    parser.add_argument("-r", "--rhost", help="usage report for the given remote host IP")
    parser.add_argument("-t","--type", type=str, choices=['daily','weekly'], help="type of report: daily or weekly")
    parser.add_argument("-u", "--user", help="usage report for the given user name")
    parser.add_argument("-v","--verbose", action="store_true",help="turn on output verbosity")
    parser.add_argument("files", metavar='F', type=str, nargs='+', help="list of files to be processed, IF you issue 'last' or 'Last' as a filename it will import from the last command using the get_login_rec function")
    args=parser.parse_args()
    if args.verbose:
        print('Files to be processed:',args.files)
        print('Type of args for files',type(args.files))
        if args.user:
            print('usage report for user:',args.user)
        if args.rhost:
            print('usage report for remote host:',args.rhost)
        if args.type:
            print('usage report type:',args.type)
    
    recordlist = read_login_rec(list(args.files)) 
    if args.type:
        string = "Daily" if args.type == 'daily' else "Weekly"
        subject = args.user if args.user else args.rhost if args.rhost else None 
        string += " list for " + str(subject)
        string += "\n" + ("=" * len(string))
        print(string)
        cal_daily_usage(subject,recordlist) if (args.type == "daily") else cal_weekly_usage(subject,recordlist)

