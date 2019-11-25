#!/usr/bin/env python3
'''
   authorship declaration

   __author__ Steve Ganzulya
   __date__ November 2019
   __version__ 1.0
 
   text to describe the purpose of this script
'''
'''Demonstrate the use of the argparse module: how to retrieve the command line argument.'''

import os 
import sys
import time
import argparse


def get_login_rec():
    ''' docstring for this fucntion
    get records from the last command
    filter out the unwanted records
    add filtered record to list (login_recs)'''
    #[ put your python code for this function here ]
    login_rec = os.popen('last -Fiw').readlines()
    login_rec = [line.strip('\n') for line in login_rec]
    login_rec = login_rec[:-2] 
    login_rec = [record.strip('\n') for record in login_rec if len(record.split()) >= 15 and len(record.split()) <= 16]
    
    return login_rec
 
def read_login_rec(filelist):
    ''' docstring for this function
    get records from given filelist
    open and read each file from the filelist
    filter out the unwanted records
    add filtered record to list (login_recs)''' 
    login_rec = []
    for filename in filelist: 
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
    ''' docstring for this function
    generate daily usage report for the given 
    subject (user or remote host)'''
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
    #[ put your python code for this function here ]
    #return daily_usage

def cal_weekly_usage(subject,login_recs):
    ''' docstring for this function
    generate weekly usage report for the given 
    subject (user or remote host)'''
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
    #[ put your python code for this function here ]
    #return weekly_usage
     
def normalized_rec(rec):
    '''Normalize login record produced by the last command.
       The login and logout time could be or not be on the same day.
       eg: (1) Mon Jan 01 12:23:34 2018 - Mon Jan 01 22:11:00 2018 
       or  (2) Mon Jan 01 23:10:45 2018 - Tue Jan 02 00:15:43 2018
       or  (3) Mon Jan 01 09:00:23 2018 - Fri Jan 05 17:00:07 2018
       The login and logout time for (1) are on the same day, this 
       record does not need to be normalized.
       The login and logout time for (2) are on two different days,
       after normalization, two records will be generated:
           (a) Mon Jan 01 23:10:45 2018 - Mon Jan 01 23:59:59 2018
           (b) Tue Jan 02 00:00:00 2018 - Tue Jan 02 00:15:43 2018

       The login and logout time for (2) spawn 5 days, after
       normalization, 5 records will be generated:
           (a) Mon Jan 01 09:00:23 2018 - Mon Jan 01 23:59:59 2018
           (b) Tue Jan 02 00:00:00 2018 - Tue Jan 02 23:59:59 2018
           (c) Wed Jan 03 00:00:00 2018 - Wed Jan 03 23:59:59 2018
           (d) Thu Jan 04 00:00:00 2018 - Thu Jan 04 23:59:59 2018
           (e) Fri Jan 05 00:00:00 2018 - Fri Jan 05 17:00:07 2018

          same day -> retrun the same record
          different days: 1st record -> keep login date/time
                                        change logout date 
                                        (update fields 9,10,11,12) 
                                        logout time-> 23:59:59
                          2nd record -> login day  +1 (update fields 3,4,5,7)
                                        time -> 00:00:00
                                        keep logout date/time
          pass the 2nd record to the normalized_rec function again
          Please note that this is a recursive function.
    ''' 
    jday = time.strftime('%j',time.strptime(' '.join(rec[4:6]+rec[7:8]),'%b %d %Y'))
    jday2 = time.strftime('%j',time.strptime(' '.join(rec[10:12]+rec[13:14]), '%b %d %Y'))
    if jday == jday2:
       norm_rec = []
       norm_rec.append(rec.copy())
       return norm_rec
    else:
       # calculate next day string in 'WoD Month Day HH:MM:SS YYYY'
       new_rec1 = rec.copy()
       new_rec = rec.copy()
       t_next = time.mktime(time.strptime(' '.join(new_rec1[4:6]+rec[7:8]),'%b %d %Y'))+86400
       next_day = time.strftime('%a %b %d %H:%M:%S %Y',time.strptime(time.ctime(t_next))).split()
       new_rec1[12] = '23:59:60'
       new_rec1[9] = new_rec1[3]
       new_rec1[10] = new_rec1[4]
       new_rec1[11] = new_rec1[5]
       new_rec[3] = next_day[0] # Day of week Sun, Mon, Tue...
       new_rec[4] = next_day[1] # Month Jan, Feb, Mar, ...
       new_rec[5] = next_day[2] # Day of Month 01, 02, ...
       new_rec[6] = next_day[3] # Time HH:MM:SS
       new_rec[7] = next_day[4] # Year YYYY
       norm_rec = normalized_rec(new_rec)
       normalized_recs = norm_rec.copy()
       normalized_recs.insert(0,new_rec1)  # call normalized_rec function recursive
    return normalized_recs
      
if __name__ == '__main__':
    
    #[ code to retrieve command line argument using the argparse module [
    parser = argparse.ArgumentParser(description="Usage Report based on the last command",epilog="Copyright 2018 - Steve Ganzulya")
    parser.add_argument("-l", "--list", type=str, choices=['user','host'], help="generate user name or remote host IP from the given files")
    parser.add_argument("-r", "--rhost", help="usage report for the given remote host IP")
    parser.add_argument("-t","--type", type=str, choices=['daily','weekly'], help="type of report: daily or weekly")
    parser.add_argument("-u", "--user", help="usage report for the given user name")
    parser.add_argument("-v","--verbose", action="store_true",help="turn on output verbosity")
    parser.add_argument("files", metavar='F', type=str, nargs='+', help="list of files to be processed")
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
    
    recordlist = get_login_rec()
    recordlist += read_login_rec(list(args.files)) 
    if args.type:
        string = "Daily" if args.type == 'daily' else "Weekly"
        subject = args.user if args.user else args.rhost if args.rhost else None 
        string += " list for " + str(subject)
        string += "\n" + ("=" * len(string))
        print(string)
        cal_daily_usage(subject,recordlist) if (args.type == "daily") else cal_weekly_usage(subject,recordlist)

