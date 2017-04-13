# -*- coding: utf-8 -*-
"""
Created on Tue May 31 22:53:13 2016

@author: qing.liu
"""
import MySQLdb

class SkuSelector:
    DISP_NUM = 5
    userHist = {}
    
    def Sort(self, matchResults):
        matchResults.sort(reverse=True, key=lambda x:x[1]+x[2])  # 改变原有对象
          
    def GuessBestSku(self, user, query, click_time):
        games = WordProcessor().skuKeywords.keys()
        matchResults = []
        for i in range(len(games)):
            wordsScore = SkuMatcher().GetSkuQuerySim(games[i], query)
            cfScore = CF().GetCFValue(games[i], user, click_time)
            if (user in self.userHist ) and ( games[i] in self.userHist[user]):
                wordsScore = 0; cfScore = 0
            matchResults.append((games[i], wordsScore, cfScore))
        self.Sort(matchResults)
        skus = ''
        for i in range(self.DISP_NUM):
            skus += " " + matchResults[i][0]
        return skus + '\n'
        
    def LoadHist(self):
        db = DBManager()
        db.cur.execute("select user,sku from train")
        results = db.cur.fetchall()
        for row in results:
            self.userHist.setdefault(row[0], [])
            if row[1] not in self.userHist[row[0]]:
                self.userHist[row[0]].append(row[1])
        db.dbclose()
        
    def Query(self):
        db = DBManager()
        db.cur.execute("select * from test")
        results = db.cur.fetchall()
        outcome = []
        for row in results:
            user = row[0]; query = row[3]; click_time = row[4]
            skus = self.GuessBestSku(user, query, click_time)
            outcome.append(skus)
        fo = open(r'D:\py\app_learn\predictions.txt', "w")
        fo.writelines(outcome)
        fo.close()
        db.dbclose()
      
