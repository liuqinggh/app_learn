# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 10:45:53 2016

@author: qing.liu
"""

# 处理基本数据

import pandas as pd
import numpy as np
from datetime import *
import scipy.spatial.distance as dist
import os

pth_raw = os.getcwd() + '\\'
#df = pd.read_csv(pth, sep = ' ')

# 读取源数据
df = pd.read_csv(pth_raw + 'raw_data.csv', sep = ',')

click_num = df.shape[0]                    # 记录数
user_num = len(df['user'].unique())        # 用户数
sku_num = len(df['sku'].unique())          # 产品数

basetick = datetime(2011, 8, 11)           #基准时间
simMatrix = np.zeros((sku_num, sku_num))   #相似度矩阵

# 处理字段
def to_dicts(df, nm):
    users = df[nm].unique()
    dff = pd.Series(users, name = nm).reset_index()   #.set_index(nm)
    dff.columns = [nm+'_id', nm]
    return dff

users = to_dicts(df, 'user')     # 用户标记
users.to_csv(pth_raw  + 'user_name.txt', index = False, float_format = '%s' )

skus = to_dicts(df, 'sku')       # 产品标记
skus.to_csv(pth_raw  + 'sku_name.txt', index = False, float_format = '%d')

# 获取日期，时间
df['click_dt'] = df['click_time'].apply(lambda x : (datetime.strptime(x, '%Y-%m-%d %H:%M:%S')- basetick).days/3 )
df['click_tm'] = df['click_time'].apply(lambda x : datetime.strftime(datetime.strptime(x, '%Y-%m-%d %H:%M:%S'), '%H'))

dd = pd.merge(df, users, on='user')
result = pd.merge(dd, skus, on='sku')

click_info = result[['user_id', 'sku_id', 'click_dt', 'click_tm']]
click_info.to_csv(pth_raw  + 'click_info.txt', index = False)

#  产品相似度矩阵
click = click_info.pivot_table(values ='click_dt', index= 'sku_id', columns='user_id', aggfunc = 'count')

# 将列内容替换成列名
for i in range(len(click.columns)):
    c = click.iloc[:,i]
    c[c> 0] = click.columns[i]

click_matrix = click.as_matrix()

for i in range(sku_num):                 #产品相似度
    for j in range(sku_num):
        simMatrix[i, j] = 1- dist.pdist([click_matrix[i, :] , click_matrix[j, :]], metric ='jaccard')  
np.savetxt(pth_raw  + 'simMatrix.txt', simMatrix, delimiter=',', fmt = '%2f')

# 每个sku在每天占比
sku_dt = click_info.pivot_table(values ='user_id', index= 'sku_id', columns='click_dt', aggfunc = 'count').fillna(0)
sku_per_dt = sku_dt.div(sku_dt.sum(axis = 1), axis = 0)
sku_per_dt.to_csv(pth_raw  + 'sku_count_by_day.txt', index = False, float_format = '%s' )

# 每个sku在每个时刻占比
sku_tm = click_info.pivot_table(values ='user_id', index= 'sku_id', columns='click_tm', aggfunc = 'count').fillna(0)
sku_per_tm = sku_tm.div(sku_tm.sum(axis = 1), axis = 0)
sku_per_tm.to_csv(pth_raw  + 'sku_count_by_hour.txt', index = False, float_format = '%s')











