#!/usr/bin/env python
#encoding:utf-8
_author_ = 'Chocolee'
import sys
import re
from RedisClass import *

def confFile(conffile):
    f = file(conffile,'r')
    for line in f.readlines():
        line = re.findall(r'\w*redis\w*',line.strip())
        print line

confFile('tsckagd.conf')
