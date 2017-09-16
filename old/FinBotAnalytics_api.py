import os
import sys
import json
import numpy as np
import pandas as pd
from configparser import RawConfigParser
from flask import Flask, jsonify

# Define paths:-----------------------------------------------------------------------------------------
basePath = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) # project root directory
dataPath = os.path.join(basePath,"data")
configPath = os.path.join(basePath,"config")
modelPath = os.path.join(basePath,"model")
scriptPath = os.path.dirname(__file__)

# Set basePaths:----------------------------------------------------------------------------------------
os.chdir(basePath)
sys.path.append(basePath)

# Read Configuration File:------------------------------------------------------------------------------
# config.read(os.path.join(configPath, 'config.ini'))
# port = int(config['ports']['application_port'])

# Load custom modules:----------------------------------------------------------------------------------
# from finbotAnalytics import TechnicalIndicator 

app = Flask(__name__)

@app.route('/welcome')
def Welcome():
    return "Welcome to MUST (https://www.must.co.in/)" 

# @app.route('/data')
def readData(fileName):
    df = pd.read_csv(os.path.join(dataPath, fileName), sep=",", header='infer', index_col=None)
    df.to_json(orient='records')
    print(df.head(n=10))
    return df

df = readData('500209.csv')

@app.route('/onBalanceVolume', methods=['GET'])
def onBalanceVolume(df):
    closingPrice = df["Close Price"].tolist()
    volume = df["Total Traded Quantity"].tolist()
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
    
@app.route('/test', methods=['POST'])
def testSum(**kwargs):
    try:
        x = kwargs['x'].strip()
    except:
        x = ""
    try:
        y = kwargs['y'].strip()
    except:
        y = ""
    
    message = {'message':x+y}
    return jsonify(int(x) + int(y))
        
if __name__ == "__main__":
    app.run()