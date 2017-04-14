# -*- coding: utf-8 -*-
"""
Created on Sun May 08 22:35:33 2016

@author: qing.liu
"""
import cProfile
import os

pth_glb = os.getcwd() + '\\' + 'result_global.txt'
pth_lcl = os.getcwd() + '\\' + 'result_local.txt'

if __name__ =="__main__":
    if os.path.exists(pth_glb): os.remove(pth_glb)
    if os.path.exists(pth_lcl): os.remove(pth_lcl)
    wp = WordProcessor()
    wp.BuildWordGraph('train')
    wp.FindConnections()
    wp.BuildGlobalEquGraph()
    wp.BuildLocalEquGraph()
    cf = CF()
    cf.Initialize()
    SkuSelector().Query()
    #cProfile.run("SkuSelector().Query()")


            