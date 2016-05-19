#!/usr/bin/env python
#encoding:utf-8
author_ = 'Chocolee'

from SqliteClass import *

db = SqliteClass('tsck.db')

print db.query('select * from public')