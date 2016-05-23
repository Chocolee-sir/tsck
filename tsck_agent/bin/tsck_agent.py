#!/usr/bin/env python
# encoding:utf-8
__author__ = 'Chocolee'
import sys
sys.path.append("..")
import threading
import time
from lib.GetRedisConfig import *
from lib.ModStatusClass import *
from lib.WatcherClass import *
from lib.RedisClass import *


#get localhost ip.
def getLocalIpAddress():
    ip = os.popen("ifconfig|awk -F '[: ]+' 'NR==2 {print $4}'").read().strip()
    return ip


#get localhost mod info.
def getLocalModInfo(modtype):
    R = RedisClass(getRedisConf()[0],int(getRedisConf()[1]))
    ModInfo = eval(R.getKey(modtype))
    try:
        localModInfo = ModInfo[getLocalIpAddress()]
    except:
        localModInfo = []
    return localModInfo


#daemon process
def loopRunProcess(localInfoList,modtype,redisConnect,frequency):
    redisExpireTime = 30
    while 1:
            tmpModstatus = {}
            for i in localInfoList:
                i = i.split(':')
                s = ModStatusClass(i[0],i[1],i[2])
                redisKey = '%s_%s_%s' %(getLocalIpAddress(),i[0],i[2])
                tmpModstatus[redisKey] = s.modStatus(modtype)
            try:
                redisConnect.batchExpireSetKey(tmpModstatus,redisExpireTime)
            except:
                print('Connect to redis error!')
                exit(1)
            time.sleep(frequency)


def setModStatusToRedis():
    modType = ['teatalkinfo','publicinfo']
    redisConnect = RedisClass(getRedisConf()[0],int(getRedisConf()[1]))
    frequency = int(getRedisConf()[-1])
    teatalkList = getLocalModInfo(modType[0])
    publicList = getLocalModInfo(modType[1])
    if len(teatalkList) != 0 and len(publicList) == 0:
        loopRunProcess(teatalkList, modType[0], redisConnect, frequency)
    elif len(teatalkList) == 0 and len(publicList) != 0:
        loopRunProcess(publicList, modType[1], redisConnect, frequency)
    elif len(teatalkList) != 0 and len(publicList) != 0:
        Watcher()
        thread1 = threading.Thread(target=loopRunProcess, args=(teatalkList, modType[0], redisConnect, frequency,))
        thread2 = threading.Thread(target=loopRunProcess, args=(publicList, modType[1], redisConnect, frequency,))
        thread1.start()
        thread2.start()
    else:
        print('This ipaddress redis module list config is none,please check it.')
        exit(1)


if __name__ == '__main__':
    try:
        setModStatusToRedis()
    except KeyboardInterrupt:
        print('  Ctrl+C ')



