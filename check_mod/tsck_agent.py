#!/usr/bin/env python
# encoding:utf-8
__author__ = 'Chocolee'
import time
from GetRedisConfig import *
from RedisClass import *
from ModStatusClass import *

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


def loopRunProcess(localInfoList,modtype,redisConnect,frequency):
    while 1:
            tmpModstatus = {}
            for i in localInfoList:
 		i = i.split(':')
                s = ModStatusClass(i[0],i[1],i[2])
                redisKey = '%s_%s_%s' %(getLocalIpAddress(),i[0],i[1])
                tmpModstatus[redisKey] = s.modStatus(modtype)
            try:
                redisConnect.batchSetKey(tmpModstatus)
            except:
                print('Connect to redis error!')
                exit(1)
            time.sleep(frequency)


def setModStatusToRedis():
    redisConnect = RedisClass(getRedisConf()[0],int(getRedisConf()[1]))
    frequency = int(getRedisConf()[-1])
    teatalkLocalInfoList = getLocalModInfo('teatalkinfo')
    publicLocalInfoList = getLocalModInfo('publicinfo')
    if len(teatalkLocalInfoList) != 0 and len(publicLocalInfoList) == 0:
        loopRunProcess(teatalkLocalInfoList,'teatalkinfo',redisConnect,frequency)
    elif len(teatalkLocalInfoList) == 0 and len(publicLocalInfoList) != 0:
        loopRunProcess(teatalkLocalInfoList,'publicinfo',redisConnect,frequency)
    elif len(teatalkLocalInfoList) != 0 and len(publicLocalInfoList) != 0:
        loopRunProcess(teatalkLocalInfoList,'teatalkinfo',redisConnect,frequency)
        loopRunProcess(teatalkLocalInfoList,'publicinfo',redisConnect,frequency)
    else:
        print('mod list none!')


if __name__ == '__main__':
    setModStatusToRedis()



