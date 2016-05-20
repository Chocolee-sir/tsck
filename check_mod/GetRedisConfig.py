#!/usr/bin/env python
#encoding:utf-8
_author_ = 'Chocolee'
import ConfigParser

#get config file
def confFile(conffile,key):
    cf = ConfigParser.ConfigParser()
    cf.read(conffile)
    try:
        return cf.get("global",key)
    except:
        return None


#get config info.
def getRedisConf():
    redis_host = confFile('tsckagd.conf','redis_host')
    redis_port = confFile('tsckagd.conf','redis_port')
    redis_mon_frequency = confFile('tsckagd.conf','redis_mon_frequency')
    if redis_host is None:
        print("Tsckagd,conf 'redis_host' configuration error,please check it.")
        exit(1)
    elif redis_port is None:
        print("Tsckagd,conf 'redis_port' configuration error,please check it.")
        exit(1)
    elif redis_mon_frequency is None:
        redis_mon_frequency = '10'
    tmpList = [redis_host,redis_port,redis_mon_frequency]
    return tmpList



