#!/usr/bin/env python
#encoding:utf-8
_author_ = 'Chocolee'
import redis

class RedisClass(object):

    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.conn = redis.ConnectionPool(host=self.host, port=self.port)
        self.pool = redis.Redis(connection_pool=self.conn)


    def setKey(self,key,value):
        try:
            self.pool.set(key,value)
        except:
            print('Connect redis error,please check redis server is normal.')
            exit(1)


    def setExpireKey(self,key,value,expiretime):
        try:
            self.pool.set(key,value)
            self.pool.expire(key,expiretime)
        except:
            print('Connect redis error,please check redis server is normal.')
            exit(1)


    def getKey(self,key):
        try:
            return self.pool.get(key)
        except:
            print('Connect redis error,please check redis server is normal.')
            exit(1)


    def batchSetKey(self,dictlist):
        try:
            pipe = self.pool.pipeline()
            for k,v in dictlist.items():
                pipe.set(k,v)
            pipe.execute()
        except:
            print('Connect redis error,please check redis server is normal.')
            exit(1)


    def batchExpireSetKey(self,dictlist,expireTime):
        try:
            pipe = self.pool.pipeline()
            for k,v in dictlist.items():
                pipe.set(k,v)
                pipe.expire(k,expireTime)
            pipe.execute()

        except:
            print('Connect redis error,please check redis server is normal.')
            exit(1)

