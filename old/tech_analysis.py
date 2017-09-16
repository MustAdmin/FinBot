# -*- coding: utf-8 -*-
"""
Created on Tue May 02 23:36:10 2017

@author: Admin
"""

import numpy as np
import pandas as pd

data = pd.read_csv('E:\MUST\FinBot-master\data\infy_mar1_31apr_data.csv')

data.head()
data.shape

## We are coding for 5 technical indicators in python
##  1. On Balance Volume (OBV)
##  2. Average Directional Index (ADI)
##  3. Moving Average Convergence Divergence
##  4. Relative Strength Index


## Writing the code for OBV

data['Date'].iloc[0]
data.dtypes


data['OBV'] = 0

for i in range(0,len(data)-1,1):
    if data['Close Price'].loc[i+1] > data['Prev Close'].loc[i+1]:
        data['OBV'].loc[i+1] = data['Total Traded Quantity'].loc[i+1] + data['OBV'].loc[i]
    elif data['Close Price'].loc[i+1] < data['Prev Close'].loc[i+1]:
        data['OBV'].loc[i+1] = data['OBV'].loc[i] - data['Total Traded Quantity'].loc[i+1]
    else: 
        data['OBV'].loc[i+1] = data['OBV'].loc[i]
        
        
        
    
    
    
data.head()


## Writing code for average directional index

# Calculating average true rate

data.head()

data['H-L'] = data['High Price'] - data['Low Price']
data['H-Cp'] = abs(data['High Price'] - data['Close Price'])
data['L-Cp'] = abs(data['Low Price'] - data['Close Price'])
data['TR'] = data[['H-L','H-Cp','L-Cp']].max(axis=1)

data['+DM 1'] = 0

for i in range(0,len(data)-1,1):
    if data['High Price'].loc[i+1] - data['High Price'].loc[i] > data['Low Price'].loc[i] -data['Low Price'].loc[i+1]:
        data['+DM 1'].loc[i+1] = max(data['High Price'].loc[i+1] - data['High Price'].loc[i],0)
    else:
        data['+DM 1'].loc[i+1] = 0
            

data['-DM 1'] = 0
for i in range(0,len(data)-1,1):
    if data['High Price'].loc[i+1] - data['High Price'].loc[i] < data['Low Price'].loc[i] -data['Low Price'].loc[i+1]:
        data['-DM 1'].loc[i+1] = max(data['Low Price'].loc[i] -data['Low Price'].loc[i+1],0)
    else:
        data['-DM 1'].loc[i+1] = 0

## Calculating TR14
data['TR14'] = 0
data['TR14'].loc[13] = data['TR'].loc[0:13].sum()   

for i in range(14,len(data),1):
    data['TR14'].loc[i] = data['TR14'].loc[i-1] - data['TR14'].loc[i-1]/14 + data['TR'].loc[i] 
data.tail()

import os
os.getcwd()
os.chdir("E:\MUST\FinBot-master")

data.to_pickle("E:\MUST\FinBot-master\data.pkl")    
data.head()
data.tail()


## Calculating DMs
data['+DM14'] = 0
data['+DM14'].loc[13] = data['+DM 1'].loc[0:13].sum()

for i in range(14,len(data),1):
    data['+DM14'].loc[i] = data['+DM14'].loc[i-1] - data['+DM14'].loc[i-1]/14 + data['+DM14'].loc[i] 
data.tail()

data['-DM14'] = 0
data['-DM14'].loc[13] = data['-DM 1'].loc[0:13].sum()

for i in range(14,len(data),1):
    data['-DM14'].loc[i] = data['-DM14'].loc[i-1] - data['-DM14'].loc[i-1]/14 + data['-DM14'].loc[i] 
data.tail()

data['+DI14'] = 100*(data['+DM14'] / data['TR14'])
data['-DI14'] = 100*(data['-DM14'] / data['TR14'])
data['DI14diff'] = data['+DI14'] - data['-DI14']     
data['DI14diff'] = data['DI14diff'].abs()

data['DI14sum'] = data['+DI14'] + data['-DI14'] 

data['DX'] = data['DI14diff']/data['DI14sum']
data['DX'].values_counts()

### Writing codes for RSI

data['change'] = 0

for i in range(0,len(data)-1,1):
    data['change'].loc[i+1] = data['Close Price'].loc[i+1] - data['Close Price'].loc[i] 

data['gain'] = 0

for i in range(0,len(data)-1,1):
    if data['change'].loc[i] > 0:
        data['gain'].loc[i] = data['change'].loc[i] 
    else:
        data['gain'].loc[i] = 0

data['loss'] = 0
for i in range(0,len(data)-1,1):
    if data['change'].loc[i] < 0:
        data['loss'].loc[i] = data['change'].loc[i] 
    else:
        data['loss'].loc[i] = 0


data['average gain'] = 0
data['average gain'].loc[13] = np.mean(data['gain'].loc[0:13])    
for i in range(14,len(data),1):
    data['average gain'].loc[i] = (data['gain'].loc[i-1]*13 + data['gain'].loc[i])/14 
          


data['average loss'] = 0
data['average loss'].loc[13] = np.mean(data['loss'].loc[0:13])    
for i in range(14,len(data),1):
    data['average loss'].loc[i] = (data['loss'].loc[i-1]*13 + data['loss'].loc[i])/14 

data['RS'] = data['average gain'] / data['average loss']

data['RSI'] = 0
for i in range(0,len(data)-1,1):
    if data['average loss'].loc[i] == 0:
        data['RSI'].loc[i] = 0 
    else:
        data['RSI'].loc[i] = 100 - 100/(1+data['RS'].loc[i])


    