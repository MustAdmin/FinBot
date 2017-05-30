import os
import sys
import json
import numpy as np
import pandas as pd 
from configparser import RawConfigParser

#-------- define paths -----------#
basePath = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) # project root directory
dataPath = os.path.join(basePath, "data")
configPath = os.path.join(basePath, "config")
modelPath = os.path.join(basePath, "model")
scriptPath = os.path.dirname(__file__)

#-------- set basePath ----------#
os.chdir(basePath)
sys.path.append(basePath)

class TechnicalIndicator(object):
    def __init__(self):
        pass
    
    def readData(self, fileName):
        df = pd.read_csv(os.path.join(dataPath, fileName), sep=",", header='infer', index_col=None)
        return df
        
    def exponentialMovingAverage(self, dataFrame, span):
        ema = []
        closingPrice = dataFrame["Close Price"].tolist()
        k = 2/(span + 1)
        ema_prev = np.mean(closingPrice[:span])
        for i in range((span + 1), len(closingPrice)):
            ema_today = (closingPrice[i-1] * k) + (ema_prev * (1-k))
            ema.append(ema_today)
            ema_prev = ema_today
        return ema
        
    def onBalanceVolume(self, dataFrame):
        closingPrice = dataFrame["Close Price"].tolist()
        volume = dataFrame["No.of Shares"].tolist()
        obv = []
        obv_start = 0

        for i in range(1,len(volume)):
            if closingPrice[i] > closingPrice[i-1]:
                obv_current = obv_start + volume[i]
                obv.append(obv_current)
            elif closingPrice[i] < closingPrice[i-1]:
                obv_current = obv_start - volume[i]
                obv.append(obv_current)
            else:
                obv_current = obv_start
                obv.append(obv_current)
            obv_start = obv_current # obv update
        return obv
        
    def relativeStrengthIndex(self, dataFrame):
        pass
        
    def averageDirectionalMovementIndex(self, dataFrame):
        pass