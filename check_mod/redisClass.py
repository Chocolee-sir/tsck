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
        self.pool.set(key,value)


    def getKey(self,key):
        return self.pool.get(key)


    def batchSetKey(self,dictlist):
        pipe = self.pool.pipeline()
        for k,v in dictlist.items():
            pipe.set(k,v)
        pipe.execute()

