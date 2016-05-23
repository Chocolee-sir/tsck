#!/usr/bin/env python
#encoding:utf-8
_author_ = 'Chocolee'
import signal,os,sys

class Watcher():
    def __init__(self):
         """ Creates a child thread, which returns.  The parent
             thread waits for a KeyboardInterrupt and then kills
             the child thread.
         """
         self.child = os.fork()
         if self.child == 0:
             return
         else:
             self.watch()

    def watch(self):
         try:
             os.wait()
         except KeyboardInterrupt:
             # I put the capital B in KeyBoardInterrupt so I can
             # tell when the Watcher gets the SIGINT
             print 'KeyBoardInterrupt'
             self.kill()
             sys.exit()

    def kill(self):
         try:
             os.kill(self.child, signal.SIGKILL)
         except OSError: pass