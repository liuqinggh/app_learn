# -*- coding: utf-8 -*-
"""
Created on Tue May 31 22:40:07 2016

@author: qing.liu
"""
import MySQLdb   
        
class DBManager:       
    def __init__(self):
        self.conn = MySQLdb.connect(host='localhost',user='root',passwd='111111',db='test',port=3306)
        self.cur = self.conn.cursor()
            
    def Createdb(self, tableName):
        try:
            self.cur.execute("drop table if exists %s"% tableName)
            self.cur.execute("create table %s (user VARCHAR(128), sku VARCHAR(32), category VARCHAR(32), query VARCHAR(255),  click_time TIMESTAMP, query_time TIMESTAMP)"%tableName)
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        print "%s is created !" %(tableName)
    
    def InsertItem(self, user, sku, category, query, click_time, query_time, tableName):
        try:
            self.cur.execute('insert into %s(user, sku, category, query, click_time, query_time) values("%s","%s","%s","%s","%s","%s")'\
            %(tableName, user, sku, category, query, click_time, query_time))
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            
    def dbclose(self):
        self.cur.close()
        self.conn.commit()
        self.conn.close()
        