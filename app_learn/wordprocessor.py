    # -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 22:59:40 2016

@author: qing.liu
"""

pth_glb = r'D:\py\app_learn\result_global.txt'
pth_lcl = r'D:\py\app_learn\result_local.txt'

pth_glb_txt = r'D:\py\app_learn\result_global.txt'
pth_lcl_txt = r'D:\py\app_learn\result_local.txt'

import math

class WordNode:
    def __init__(self):
        self.pre = set(); self.nextNode = set()            #每个单词的前驱后继集合
        self.cnt = 0;   self.groupID = 0                      #单词出现次数、所在网络编号
        self.neighbours = set()                               #单词的所有可能的替换词 
        self.correctWord = ''                             #该单词对应的正确的单词                
        
    def Tick(self):
        self.cnt += 1
        
    def TryAddNeighbour(self, word):
        if word not in self.neighbours:
            self.neighbours.add(word)
            
    def TryAddPre(self, word):
        if word not in self.pre:
            self.pre.add(word)
    
    def TryAddNext(self, word):
        if word not in self.nextNode:
            self.nextNode.add(word)
            
    def CountOverlap(self, a, b):
        self.cnt = 0
        for word in a:
            if (word in b) : self.cnt+=1
        return self.cnt

class WordProcessor:
    MAX_EDIT_DIST = 2
    MIN_DELTA =10
    globalDict = {}
    skuKeywords = {}
    skuVersion = {}
    skuMaxWordCnt = {}
    
    def OutputConnections(self, worddict, filename, sku):
        doc = open(filename, 'a+')
        doclist = []
        words = worddict.keys()
        lenw = len(words)
        for i in range(lenw-1):
            if len(words[i]) >= Tools().MIN_WORD_LENGTH:
                for j in range(i+1, lenw):
                    if len(words[j]) < Tools().MIN_WORD_LENGTH: continue
                    if Tools().ISEditDistOK(words[i], words[j]):
                        x = self.GetOrAddNode(worddict, words[i])
                        y = self.GetOrAddNode(worddict, words[j])
                        t = Tools().GetWordSim(x, y)
                        doclist.append(sku +"," +words[i] + "," +words[j] + "," + str(t) + "," + str(x.cnt) + "," + str(y.cnt)+ '\n')
        doc.writelines(doclist)
        doc.close()
        
    def FindConnections(self):
        self.OutputConnections(self.globalDict, pth_glb_txt, "")
        for sku, x in self.skuKeywords.items():
            self.OutputConnections(self.skuKeywords[sku], pth_lcl_txt, sku)
            
    def FindCorrectWord(self, word, groupID, visited, wdict):
        best = word
        maxCnt = wdict[word].cnt
        for key in wdict[word].neighbours:
            if key not in visited:
                visited.add(key)
                result = self.FindCorrectWord(key, groupID, visited, wdict)
                if result[1] > maxCnt:
                    maxCnt = result[1]
                    best = result[0]
        return (best, maxCnt)
    
    def TryCorrectWords(self, wdict):  ###
        curID = 0; visited = set(); result = {}
        for key in wdict.keys():
            if key not in visited:
                word = self.FindCorrectWord(key, curID, visited, wdict)
                result[curID] = word
                wdict[key].correctWord = word[0]
                curID += 1
            else:
                word = result[wdict[key].groupID]
                wdict[key].correctWord = word[0]

    def TryAddRelation(self, wdict, a, b):
        x = self.GetOrAddNode(wdict, a)
        y = self.GetOrAddNode(wdict, b)
        x.TryAddNeighbour(b)
        y.TryAddNeighbour(a)
        
    def BuildEquivalenceGraph(self, relations, wdict):
        for i in range(len(relations)):
            if (relations[i][2] > 0 and abs(int(relations[i][3]) - int(relations[i][4])) > self.MIN_DELTA):
                self.TryAddRelation(wdict, relations[i][0], relations[i][1])
    
    def BuildGlobalEquGraph(self):
        a = open(pth_glb_txt).readlines()
        relations = []
        for i in range(len(a)):
            words = a[i].strip('\n').split(',')
            relations.append(words)
        self.BuildEquivalenceGraph(relations, self.globalDict)
        self.TryCorrectWords(self.globalDict)
        
    def BuildLocalEquGraph(self):
        a = open(pth_lcl_txt).readlines()
        pre = 'hello world'
        slist = []
        for i in range(len(a)):
            words = a[i].strip('\n').split(',')
            if words[0] != pre:
                if len(slist) > 0:
                    self.BuildEquivalenceGraph(slist, self.GetOrAddDict(pre));
                    self.TryCorrectWords(self.GetOrAddDict(pre))
                pre = words[0]
                slist = []
            slist.append(words)
        if len(slist) >0:
            self.BuildEquivalenceGraph(slist, self.GetOrAddDict(pre))
            self.TryCorrectWords(self.GetOrAddDict(pre))

    def GetOrAddDict(self, sku):  # word
        self.skuKeywords.setdefault(sku, {})
        return self.skuKeywords[sku]

    def GetOrAddNode(self, wdict, word):
        wdict.setdefault(word, WordNode())
        return wdict[word]
   
    def AddVersion(self, sku, v):
        sdict = {}
        if sku in self.skuVersion:
            sdict = self.skuVersion[sku]
        else:
            self.skuVersion[sku] = sdict 
        sdict.setdefault(v, 0)
        sdict[v] += 1
            
    def AddQueryWords(self, sku, query):
        words = Tools().CleanWords(query)
        if (words == None or len(words) == 0): return
        wdict = self.GetOrAddDict(sku)
        for i in range(len(words)):
            if len(words[i]) == 0 :continue
            node = self.GetOrAddNode(wdict,  words[i])
            node.Tick()
            if (i > 0):
                node.TryAddPre(words[i - 1])
            if i < (len(words) -1):
                node.TryAddNext(words[i + 1])
            v = Tools().TryGetInt(words[i])
            if (v > 0 and v < 20):
                self.AddVersion(sku, v)
            node = self.GetOrAddNode(self.globalDict, words[i])    
            node.Tick()
            if (i > 0):
                node.TryAddPre(words[i - 1])
            if (i < (len(words) - 1)):
                node.TryAddNext(words[i + 1])

    def BuildWordGraph(self, tableName): # 3个全局变量
        db = DBManager()
        sql_txt = "select sku, query from %s" % tableName
        db.cur.execute(sql_txt)
        results = db.cur.fetchall()
        for row in results:
            sku = row[0]
            query = row[1]
            self.AddQueryWords(sku, query)
        for sku in self.skuKeywords.keys():
            sdict = self.skuKeywords[sku]
            maxCnt = 0
            for word in sdict.keys():
                maxCnt = max(maxCnt, sdict[word].cnt)
            self.skuMaxWordCnt[sku] = maxCnt
        db.dbclose()
        
    def FindMostSimWord(self, sdict, key):
        if len(key) < Tools().MIN_WORD_LENGTH : return key
        words = sdict.keys()
        ans = key
        maxcnt = 0
        for i in range(len(words)):
            if len(words[i]) >= Tools().MIN_WORD_LENGTH:
                if Tools().ISEditDistOK(words[i], key):
                    if (sdict[words[i]].cnt > maxcnt):
                        ans = words[i]
                        maxcnt = sdict[words[i]].cnt
        return ans

    def GetCorrectQuery(self, sku, query):
        words = Tools().CleanWords(query)
        if sku in self.skuKeywords:
            sdict = self.skuKeywords[sku]
            for i in range(len(words)):
                if words[i] in sdict:
                    node = sdict[words[i]]
                    words[i] = node.correctWord
                else:
                    pre = words[i]
                    words[i] = self.FindMostSimWord(sdict, words[i])
                    if ((pre == words[i]) and (words[i] in self.globalDict)):
                        words[i] = self.globalDict[words[i]].correctWord
        return words
 
