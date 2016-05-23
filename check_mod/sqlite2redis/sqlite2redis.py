#!/usr/bin/env python
#encoding:utf-8
author_ = 'Chocolee'
from SqliteClass import *
from tsck_agent.lib.RedisClass import *

db = SqliteClass('tsck.db')


def ipList(sqltype):
    tmpipList = []
    if sqltype == "teatalk":
        ipListSql = "select ip from module group by ip"
    elif sqltype == "public":
        ipListSql = "select ip from public group by ip"
    else:
        print('sqltype error!')
        exit(1)
    for i in db.queryAll(ipListSql):
        tmpipList.append(str(i[0]))
    return tmpipList


def transDict(list,sqltype):
    Dict = {}
    for ip in list:
        tmpMlist = []
        if sqltype == "teatalk":
            sql = "select modulename,CPname,port from module where ip ='%s'" %ip
        elif sqltype == "public":
             sql = "select publicname,cpname,port from public where ip ='%s'" %ip
        else:
            print('sqltype error,exit.')
            exit(1)
        for n in db.queryAll(sql):
            tmpMlist.append('%s:%s:%s' %(str(n[0]),str(n[2]),str(n[1])))
        Dict[ip] = tmpMlist
    return Dict


if __name__ == '__main__':
    dictTeatalk = transDict(ipList('teatalk'),'teatalk')
    dictPublic = transDict(ipList('public'),'public')
    R = RedisClass('10.10.206.96',6379)
    R.setKey('teatalkinfo',dictTeatalk)
    R.setKey('publicinfo',dictPublic)
 #   print eval(R.getKey('teatalkinfo'))['10.10.206.96']





