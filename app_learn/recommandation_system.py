# -*- coding: utf-8 -*-
"""
Created on Sun May 08 22:35:33 2016

@author: qing.liu
"""

import cProfile
import os

pth_glb_txt = r'D:\py\app_learn\result_global_tt.txt'
pth_lcl_txt = r'D:\py\app_learn\result_local_tt.txt'

if __name__ =="__main__":
    os.remove(pth_glb_txt)
    os.remove(pth_lcl_txt)
    wp = WordProcessor()
    wp.BuildWordGraph('train')
    wp.FindConnections()
    wp.BuildGlobalEquGraph()
    wp.BuildLocalEquGraph()
    cf = CF()
    cf.Initialize()
    cProfile.run("SkuSelector().Query()")
    #cProfile.run("SkuSelector().Query()", filename="result.out", sort="cumulative")

            