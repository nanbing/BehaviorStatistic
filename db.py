# -*- coding:utf-8 -*-
import sys
import logging
import os.path
import apsw
from datetime import datetime

log = logging.getLogger('Behavior Statistic')
log.addHandler(logging.StreamHandler())

DATABASE='%s/behaviorstatistic.db3' % os.path.dirname(os.path.abspath(__file__))
TABLE='statistic'


class Db(object):

    def __init__(self):
        self.conn=apsw.Connection(DATABASE)
        self.__create_table()

    def __create_table(self):
        self.__exec("""CREATE TABLE IF NOT EXISTS %s(
                        action text,
                        count int,
                        started_at date
                        )""" % TABLE)

    def __exec(self,s,binds=None):
        try:
            c = self.conn.cursor()
            c.execute(s,binds)
            c.close()
        except Exception,e:
            log.error(e)
        return self.conn.changes()

    def __select(self,s,binds=None):
        rs=[]
        try:
            c = self.conn.cursor()
            c.execute(s,binds)
            rs=c.fetchall()
            c.close()
        except Exception,e:
            log.error(e)
        return rs

    def __now_str(self):
        return datetime.now().strftime('%Y-%m-%d')

    def __daygap(self,started_at_str):
        tdelta=datetime.now()-datetime.strptime(started_at_str,'%Y-%m-%d')
        days=tdelta.days
        if days==0:
            days=1
        return days

    def __dataitem(self,i):
        return {'action':i[0], 'count':i[1],'started_at':i[2],'perday':float(i[1])/self.__daygap(i[2])}

    def data(self):
        rs=self.__select("SELECT action,count,started_at FROM %s ORDER BY count DESC" % TABLE)
        result=[]
        for i in rs:
            result.append(self.__dataitem(i))
        return result

    def stat(self):
        rs=self.data()
        print "Behavior Statistic"
        print "================================================================"
        print "Action\t\t\ttotal\t\tfrequency"
        print "----------------------------------------------------------------"
        for i in rs:
            print u"%s\t\t\t%s\t\t%s" % (i['action'],i['count'],i['perday'])
        print "================================================================"

    def list_action(self):
        rs=self.__select("SELECT action FROM %s" % TABLE)
        if len(rs)==0:
            print u"No Available Action,add one?"
            return
        print u"Available Actions"
        print "========================="
        for i in rs:
            print u"%s\r" % i
        print "========================="

    def add_action(self,action):
        self.__exec("""
            INSERT INTO %s (action,count,started_at)
            values(?,0,?)""" % TABLE, (action,self.__now_str()))


    def remove_action(self,action):
        if self.__exec("DELETE FROM %s WHERE action =?" % TABLE, (action,)) == 0:
            print u"Invalid Action:%s" % action
            self.list_action()

    def reset_action(self,action):
        if self.__exec("""
                UPDATE %s SET count=0,started_at=?
                WHERE action =?""" % TABLE, (self.__now_str(),action)) == 0:
            print u"Invalid Action:%s" % action
            self.list_action()

    def clear(self):
        self.__exec("DELETE FROM %s" % TABLE)

    def increase(self,action):
        self.__exec("UPDATE %s SET count=count+1 WHERE action =?" % TABLE, (action,))
    

db=Db()

