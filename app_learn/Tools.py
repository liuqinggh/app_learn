# -*- coding: utf-8 -*-
"""
Created on Wed Jun 01 23:55:01 2016

@author: qing.liu
"""

import re
from datetime import *
from time import *
import Levenshtein

class Tools:
    spliteChars = r"[A-Za-z0-9]+"
    MIN_WORD_LENGTH = 5
    
    def RemoveSpecialChar(self, word):
        word = ''.join([v for v in word if v.isdigit() or v.isalpha() or v==' '])
        return word

    def TrySplitNum(self, word):
        digit = filter(str.isdigit, word)
        alpha = filter(str.isalpha, word) 
        return alpha, digit

    def CleanWords(self, query):
        buf = re.findall(self.spliteChars, query.lower().strip())
        for i in range(len(buf)):
            buf[i] = self.RemoveSpecialChar(buf[i])
        words = buf
        for i in range(len(words)):
            if (len(words[i]) > 0 and words[i][0].isdigit() and words[i][-1].isalpha()) :
                if '2k' in words[i]:
                    continue
                else :
                    tup = self.TrySplitNum(words[i]) 
                    words[i] = tup[0]
                    words.insert(i+1, tup[1])
        return words
    
        #  编辑字符串距离       
    def ISEditDistOK(self, a, b):
        lenth = Levenshtein.distance(a, b)
        if ((len(a) < self.MIN_WORD_LENGTH ) and (len(b) < self.MIN_WORD_LENGTH)):
            return False
        elif ((len(a) == self.MIN_WORD_LENGTH ) and (len(b) == self.MIN_WORD_LENGTH)):
            if lenth <= 1 :
                return lenth 
        elif lenth <= 2:
            return lenth 
        
    def GetWordSim(self, x, y):
        return WordNode().CountOverlap(x.pre, y.pre) + WordNode().CountOverlap(x.nextNode, y.nextNode)

    def GetDayDelta(self, mtime):
        t = datetime(2011, 8, 11)
        return (mtime - t).days/3
        #return (datetime.strptime(mtime, '%Y-%m-%d %H:%M:%S') - t).days / 3

    def TryGetInt(self, word):
        if word.isdigit() :
            return word
        return self.TryConvertRome(word)

    def TryConvertRome(self, word):
        word = word.upper()
        if word == "II": return 2
        elif word == "III": return 3
        elif word == "IV" : return 4
        elif word == "V": return 5
        elif word == "VI": return 6
        elif word == "VII": return 7
        elif word == "VIII": return 8
        elif word == "IX": return 9
        elif word == "X": return 10
        elif word == "XI": return 11
        elif word == "XII": return 12
        elif word == "XIII": return 13
        elif word == "XIV": return 14
        elif word == "XV": return 15
        elif word == "XVI": return 16
        elif word == "XVII": return 17
        elif word == "XVIII": return 18
        elif word == "XIX": return 19
        else : return -1


