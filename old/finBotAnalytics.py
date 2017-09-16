# -*- coding: utf-8 -*-
"""
Analytics Module for the FinBot Project

@author: MUST Research Club (https://www.must.co.in/)
"""

import os
import sys
import json
import numpy as np
import pandas as py
from configparser import RawConfigParser

# Define paths:-----------------------------------------------------------------------------------------
basePath = os.path.dirname(os.path.dirname(os.path.realpath(_file_))) # project root directory
dataPath = os.path.join(basePath,"data")
configPath = os.path.join(basePath,"config")
modelPath = os.path.join(basePath,"model")
scriptPath = os.path.dirname(__file__)

# Set basePaths:----------------------------------------------------------------------------------------
os.chdir(basePath)
sys.path.append(basePath)

class TechnicalIndicator(object):
    def __init__(self):
        pass
    
    def readData(self, fileName):
        df = pd.read_csv(os.path.join(dataPath,fileName), sep=",",header='infer',index_col=None)
        return df

    def onBalanceVolume(self, dataFrame):
        closingPrice = dataFrame["Close Price"].tolist()
        volume = dataFrame["Total Traded Quantity"].tolist()
        obv = []
        obv_current = 0
        obv.append(obv_current)
        
        for i in range(0,len(volume)-1):
            if closingPrice[i] > closingPrice[i-1]:
                obv_current = obv_current + volume[i]
                obv.append(obv_current)
            elif closingPrice[i] < closingPrice[i-1]:
                obv_current = obv_current - volume[i]
                obv.append(obv_current)
            else:
                obv_current = obv_current
                obv.append(obv_current)
            
        return obv
    
    def avgDirIndex(self, dataFrame):
        priceRange = dataFrame["High Price"] - dataFrame["Low Price"]
        priceRange_list = priceRange.tolist()
        highPrice_closePriceDiff = abs(dataFrame["High Price"] - dataFrame["Low Price"]).tolist()
        lowPrice_closePriceDiff = abs(dataFrame["Low Price"] - dataFrame["Close Price"]).tolist()
        TrueRange = np.maximum(priceRange_list,highPrice_closePriceDiff,lowPrice_closePriceDiff)
        
        plusDM1 = []
        plusDM1_current = 0
        highPrice = dataFrame["High Price"].tolist()
        lowPrice = dataFrame["Low Price"].tolist()
        
        for i in range(0,len(highPrice)-1,1):
            if highPrice[i+1] - highPrice[i] >  lowPrice[i] - lowPrice[i+1]:
                plusDM1_current = max(highPrice[i+1] - highPrice[i],0)
            else:
                plsuDM1_current = 0
                plusDM1.append(+DM1_current)
        
        minusDM1 = [] 
        minusDM1_current = 0
        for i in range(0,len(highPrice)-1,1):
            if highPrice[i+1] - highPrice[i] < lowPrice[i] - lowPrice[i+1]:
                minusDM1_current = max(lowPrice[i] - lowPrice[i+1],0)
            else:
                minusDM1_current = 0
                minusDM1.append(-DM1_current)
        TR14 = [0]*len(highprice)
        TR14[13] = TR14[0:13].sum()
        for i in range(14,len(dataFrame),1):
            TR14[i] = TR14[i-1] - TR14[i-1]/14 + TR[i]
       
        minusDM14 = [0]*len(dataFrame)
        minusDM14[13] = minusDM1[0:13].sum() 
       
        for i in range(14,len(dataFrame)-1,1):
            minusDM14[i] - minusDM14[i-1]/14 + minusDM1[i] 
        plusDirIdx14 = [j / 100 for j in [i*100 for i in plusDM14]]
        minusDirIdx14 = [j / 100 for j in [i*100 for i in minusDM14]]
        DI14diff = [] 
        for i in range(0,len(dataFrame)-1,1):
            diff = abs(plusDirIdx14[i] - minusDirIdx14[i])
            DI14diff.append = diff
        DI14sum = []
        for i in range(0,len(dataFrame)-1,1):
            add = abs(plusDirIdx14[i] - minusDirIdx14[i])
            DI14sum.append = add
        DirIdx = []
        for i in range(0,len(dataFrame)-1,1):
            div = DI14diff[i] / DI14sum[i]
            DirIdx.append = div
        return DirIdx
       
    def RSI(self, dataFrame):
        closPrice = dataFrame['Close Price'].tolist()
        changeList = [0]*len(dataFrame)
        
        for i in range(0,len(dataFrame)-1,1):
            change = closePrice[i+1] - closePrice[i]
            changeList.append = change
        gainList = [0]*len(dataFrame)
        lossList = [0]*len(dataFrame)
        for i in range(0,len(dataFrame)-1,1):
            if changeList[i] < 0:
                lossList[i] = changeList[i]
            else:
                lossList[i] = 0
        for i in range(0,len(dataFrame)-1,1):
            if changeList[i] > 0:
                gainList[i] = changeList[i]
            else:
                gainList[i] = 0
        avgGain = [0]*len(dataFrame)
        avgLoss = [0]*len(dataFrame)
        avgLoss[13] = np.mean(lossList[0:13])
        for i in range(14,len(dataFrame)-1,1):
            
            avgLoss[i] = (lossList[i-1]*13 + lossList[i])/14
            avgGain[i] = (gainList[i-1]*13 + gainList[i])/14
        RSlist = []
        
        for i in range(14,len(dataFrame)-1,1):
            RS = avgGain[i] / avgLoss[i]
            RSlist.append = RS
        RSIdxList = [0]*len(dataFrame)
        for i in range(0,len(dataFrame)-1,1):
            if avgLoss[i] == 0:
                
                RSI = 0
            else:
                RSI = 100 - 100/(1+RS[i])
            RSIIdxList.append = RSI
            return RSIIdxList