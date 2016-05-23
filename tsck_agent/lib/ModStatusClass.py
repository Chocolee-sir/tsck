#!/usr/bin/env python
#encoding:utf-8
_author_ = 'Chocolee'
import os

class ModStatusClass():

    def __init__(self,modulename,port,cpname):
        self.modulename = modulename
        self.port = port.split(';')
        self.cpname = cpname
        while '' in self.port:
            self.port.remove('')


    def modStatus(self,modType):
        if modType == 'teatalkinfo':
            modName = '%s_%s' %(self.modulename,self.cpname.split('P')[-1])
        elif modType == 'publicinfo':
            modName = self.modulename
        else:
            print("'%s' is not exists,ModType error!" %modType)
            exit(1)
        modProcStatus = os.popen("ps -ef |grep %s|egrep -v 'sh|grep|python'|wc -l" %modName).read().strip()
        if len(self.port) == 1:
            modPortStatus = os.popen("netstat -lnutp|grep %s|wc -l" %self.port[0]).read().strip()
            if modProcStatus == '1' and modPortStatus =='1':
                return 0
            else:
                return 1
        elif len(self.port) == 2:
            modPortStatusOne = os.popen("netstat -lnutp|grep %s|wc -l" %self.port[0]).read().strip()
            modPortStatusTwo = os.popen("netstat -lnutp|grep %s|wc -l" %self.port[1]).read().strip()
            if modPortStatusOne == '1' and modPortStatusTwo =='1' and modProcStatus == '1':
                return 0
            else:
                return 1
        elif self.port == []:
            if modProcStatus == '1':
                return 0
            else:
                return 1


if __name__ == '__main__':
    P = ModStatusClass('pub_platform','8110','CP1')
    print P.modStatus('pub')
#    P = ModStatusClass('pub_message_server','','CP1')
#    print P.modStatus('pub')
#    P = ModStatusClass('cmp','8084;5000','CP2')
#    print P.modStatus('tea')
#    P = ModStatusClass('dtc','8888','CP3')
#    print P.modStatus('tea')





