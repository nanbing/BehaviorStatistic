# -*- coding:utf-8 -*-
import sys
import threading
import time
from db import db
from chart import total,frequency

USAGE= u"""
Useage
==============================================================================
add [action]
  add a new action.

remove [action]
  remove action.

reset [action]
  reset action,so count and start time of this action will be changed.

clear
  remove all data.

stat
  show statistic.

v [total|frequency]
  visualize statistic by generate a chart, frequency by default.

q
  quit
==============================================================================
"""
print USAGE

class ProgressBar(threading.Thread):

    def __init__(self,runing=True):
        threading.Thread.__init__(self, name = 'progressbar') 
        self.running=True

    def run(self):
        while self.running:
            sys.stdout.write('.')
            time.sleep(1)
        

def __quite(args):
    if len(args)==1 and args[0]=='q':
        exit(0)

def __clear(args):
    if len(args)==1 and args[0]=='clear':
        cmd=raw_input("All data will be removed and it can not be restored, are you sure?[Y/N]")
        if cmd.lower()=='y':
            db.clear()
            return True
        print 'you canceled the command.'
        return True
    return False


def __visualize_call(fn):
    pb=ProgressBar()
    pb.start()
    f=fn()
    pb.running=False
    print '%s is done' % f
    return True

def __visualize(args):

    def __is(s):
        if len(args)==1 or args[1]==s:
            return True
        return False

    if len(args)>0 and args[0]=='v':
        if __is('frequency'):
            return __visualize_call(frequency)
        if __is('total'):
            return __visualize_call(total)
    return False

def __add(args):
    if len(args)==2 and args[0]=='add':
        db.add_action(args[1])
        return True
    return False

def __remove(args):
    if len(args)==2 and args[0]=='remove':
        db.remove_action(args[1])
        return True
    return False

def __reset(args):
    if len(args)==2 and args[0]=='reset':
        db.reset_action(args[1])
        return True
    return False

def __stat(args):
    if len(args)==1 and args[0]=='stat':
        db.stat()
        return True
    return False


while True:
    cmd=raw_input('>')
    args=cmd.split()
    if __visualize(args):continue
    if __add(args):continue
    if __remove(args):continue
    if __reset(args):continue
    if __stat(args):continue
    if __clear(args):continue
    __quite(args)
    print u"invalid command: \"%s\" \r\n" % cmd
    print USAGE


