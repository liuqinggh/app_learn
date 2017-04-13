# -*- coding: utf-8 -*-
"""
Created on Tue May 31 22:46:09 2016

@author: qing.liu
"""
import math

class SkuMatcher:
    COMBO_BONUS = 0.8
    
    def GetWordPairScore(self, wdict, sku, word):
        node = wdict[word]
        return math.log(node.cnt + 1)*(node.cnt + 0.0 )/WordProcessor().skuMaxWordCnt[sku]
        
    def GetSkuQuerySim(self, sku, query):
        score = 0
        words = WordProcessor().GetCorrectQuery(sku, query)
        dict_sku = WordProcessor().skuKeywords[sku]
        for i in range(len(words)):
            if (words[i] in dict_sku):
                score += self.GetWordPairScore(dict_sku, sku, words[i])
                if i > 0:
                    node = dict_sku[words[i]]
                    if (words[i -1] in node.pre):
                        score += self.COMBO_BONUS
        return score
        