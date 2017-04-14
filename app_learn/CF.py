# -*- coding: utf-8 -*-
"""
Created on Wed Jun 01 23:59:40 2016

@author: qing.liu
"""
import MySQLdb
import numpy as np

pth_glb = os.getcwd() + '\\' + 'result_global.txt'
pth_lcl = os.getcwd() + '\\' + 'result_local.txt'
pth_sim = os.getcwd() + '\\' + "simMatrix.txt"
pth_day = os.getcwd() + '\\' + "sku_count_by_day.txt"
pth_hour = os.getcwd() + '\\' + "sku_count_by_hour.txt"

class CF:
    SKU_NUM = 413
    lambdah= 5
    userIdx = {}
    skuIdx = {}
    simMatrix = np.zeros((413, 413))
    sku_day = np.zeros((413, 28))
    sku_hour = np.zeros((413, 24))
    
    def LoadInfos(self):
        tmp = open(pth_sim).readlines()
        for i in range(413):
            line = tmp[i].strip('\r\n').split(',')
            for j in range(413):
                self.simMatrix[i, j] = line[j]
        tmp = open(pth_day).readlines()    
        for i in range(413):
            line = tmp[i].strip('\r\n').split(',')
            for j in range(28):
                self.sku_day[i, j] = line[j]
        tmp = open(pth_hour).readlines() 
        for i in range(413):
            line = tmp[i].strip('\r\n').split(',')
            for j in range(24):
                self.sku_hour[i, j] = line[j]
        print 'Load finished！'
    
    def BuildItemMatrix(self):
        db = DBManager()
        sql_txt = "select user,sku, click_time from train"
        db.cur.execute(sql_txt)
        results = db.cur.fetchall()
        for row in results:
            if row[0] not in self.userIdx:
                self.userIdx[row[0]] = len(self.userIdx)
            if row[1] not in self.skuIdx:
                self.skuIdx[row[1]] = len(self.skuIdx)
        db.dbclose()
                
    def GetCFValue(self, sku, user, time):
        score = 0
        idx = self.skuIdx[sku]
        day = Tools().GetDayDelta(time)
        hour = time.hour     #hour = datetime.strptime(time, '%Y-%m-%d %H:%M:%S').hour
        score += self.sku_day[idx, day] + self.sku_hour[idx, hour]
        userHist = SkuSelector().userHist
        if user in userHist:
            lower = 0; sumv = 0
            hist = userHist[user]
            for idd in hist:
                sku_id = self.skuIdx[idd]
                if sku_id != idx:
                    sumv += self.simMatrix[sku_id, idx]
                    lower = min(self.simMatrix[sku_id, idx], lower)
            if sumv > 0:
                sumv /= self.GetSum(idx, lower)
            score += sumv
        return score * self.lambdah
        
    def GetSum(self, sku, lowerbound): 
        ans = 0;
        for i in range(self.SKU_NUM):
            if (i != sku and self.simMatrix[sku, i] >= lowerbound):
                ans += self.simMatrix[sku, i];
        return ans;
    
    def Initialize(self):
        SkuSelector().LoadHist() 
        self.BuildItemMatrix()
        self.LoadInfos()