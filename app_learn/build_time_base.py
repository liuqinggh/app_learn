# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 10:45:53 2016

@author: qing.liu
"""

import pandas as pd
import numpy as np
from datetime import *
import math

pth = r'C:\Users\qing.liu\Desktop\baidu_movie\lecast\first\lecastwork\fudan\temp_files\clickinfo.txt'
pth_user = r'C:\Users\qing.liu\Desktop\baidu_movie\lecast\first\lecastwork\fudan\temp_files\userid.txt'
pth_sku = r'C:\Users\qing.liu\Desktop\baidu_movie\lecast\first\lecastwork\fudan\temp_files\skuid.txt'
pth_raw = r'C:\Users\qing.liu\Desktop\baidu_movie\lecast\first\lecastwork\fudan\raw_data.csv'
#df = pd.read_csv(pth, sep = ' ')


df = pd.read_csv(pth_raw, sep = ',')

click_num = df.shape[0]
user_num = len(df['user'].unique())
sku_num = len(df['sku'].unique())

click_matrix = np.zeros((sku_num, user_num))
basetick = datetime(2011, 8, 11)
users = np.empty(click_num)  #np.zeros((click_num, 1))
skus = np.empty(click_num)   #np.zeros((click_num, 1))
ticks = np.empty(click_num)  #np.zeros((click_num, 1))
#txt = open(pth).readlines()

for i in range(click_num):
    m = txt[i].strip('\n').split(' ')
    skus[i] = m[1]
    users[i] = m[0]
    date = m[2]
    time = m[3]
    click_matrix[int(skus[i])-1, int(users[i]) -1] = 1
    ticks[i] = (datetime.strptime(str(m[2]+' '+m[3]), '%Y/%m/%d %H:%M:%S') - basetick).days

#  user名称
txt = open(pth_user).readlines()
user_names = dict()
for i in range(user_num):
    m = txt[i].strip('\n').split(' ')
    user_names[i] = m[1]
pd.Series(user_names).to_csv(r'D:\py\app_learn\user_names.txt', sep = '\t')

#  sku名称
txt = open(pth_sku).readlines()
sku_names = dict()
for i in range(sku_num):
    m = txt[i].strip('\n').split(' ')
    sku_names[i] = m[1]
pd.Series(sku_names).to_csv(r'D:\py\app_learn\sku_names.txt', sep = '\t')

# 每个sku在每天的占比
sku_count_by_day = np.zeros((sku_num, 28))

ilist = [ i for i in range(0,85) if i%3 == 0]
llist = [ i for i in range(len(ilist) -1) ]

cats = pd.cut(ticks, ilist, labels=llist)
ss = pd.Series(cats).value_counts().sort_index()
sss = ss/len(ticks)
sss.to_csv(r'D:\py\app_learn\sku_count_by_day.txt', sep = '\t')


# 每个sku在每个时刻占比
sku_count_by_hour = np.zeros((sku_num, 24))

tlist = [ i for i in range(25)]
tmlist = [ i for i in range(len(tlist) -1) ]

cats = pd.cut(ticks, tlist, labels=tmlist)
skh = pd.Series(cats).value_counts().sort_index()
skhh = skh/len(ticks)
skhh.to_csv(r'D:\py\app_learn\sku_count_by_hour.txt', sep = '\t')

# getsimMatrix

import scipy.spatial.distance as dist

simMatrix = np.zeros((sku_num, sku_num))

for i in range(sku_num):
    for j in range(sku_num):
        simMatrix[i, j] = dist.pdist([click_matrix[i, :] , click_matrix[j, :]],'jaccard')  

np.savetxt(r'D:\py\app_learn\simMatrix.txt', simMatrix, delimiter='\t')











