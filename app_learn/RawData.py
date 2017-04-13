# -*- coding: utf-8 -*-
"""
Created on Wed Jun 01 23:47:42 2016

@author: qing.liu
"""

class RawData:
    def LoadRawTrainingData(self):
        pth_train = r"C:\Users\qing.liu\Desktop\baidu_movie\lecast\first\lecastwork\fudan\raw_data.csv"
        txt = open(pth_train).readlines()
        db = DBManager()
        cur = db.Createdb('train')
        for line in txt[1:]:
            m = line.strip('\n').split(',')
            db.InsertItem( m[0], m[1], m[2], m[3], m[4], m[5], 'train')
        db.dbcommit()
            
    def LoadRawTestData(self):
        pth_test = r"C:\Users\qing.liu\Desktop\baidu_movie\lecast\first\lecastwork\fudan\test_data.csv"
        txt = open(pth_test).readlines()
        db = DBManager()
        cur = db.Createdb('test')
        for line in txt[1:]:
            m = line.strip('\n').split('\t')
            db.InsertItem( m[0], '', m[1], m[2], m[3], m[4], 'test')
        db.dbcommit()

