import os
import sys
import json
import cherrypy
import numpy as np
import pandas as pd
from configparser import RawConfigParser
from flask import Flask, request

app = Flask(__name__)

# Define paths:-----------------------------------------------------------------------------------------
basePath = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) # project root directory
dataPath = os.path.join(basePath,"data")
configPath = os.path.join(basePath,"config")
modelPath = os.path.join(basePath,"model")
scriptPath = os.path.dirname(__file__)

# Set basePaths:----------------------------------------------------------------------------------------
#os.chdir(basePath)
sys.path.append(basePath)

# Load custom module:-----------------------------------------------------------------------------------
# from finbotAnalytics import TechnicalIndicator

def read_data(self, fileName):
    df = pd.read_csv(os.path.join(dataPath, fileName), sep=",", header='infer', index_col=None)
    return df



    
@app.route('/obv', methods=['POST'])
def onBalanceVolume():
    try:
        org_name = request.json['org_name'].strip()
    except:
        org_name = ''
    print("org name:", org_name)
    
    if org_name == 'infy':
        data = read_data('500209.csv')
        closingPrice = data["Close Price"].tolist()
        volume = data["Total Traded Quantity"].tolist()
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
        return json.dumps("On balance volume is " + str(obv))
    else:
        return json.dumps("On balance volume is not available for this organization")
    
    
# def GetTechIndicator(self, **kwargs):
    # try:
        # fileName = kwargs["fileName"].strip()
    # except Exception:
        # fileName = ""
    # try:
        # purpose = kwargs["purpose"].strip()
    # except Exception:
        # purpose = ""
    
    # if fileName and purpose:
        # ti = TechnicalIndicator()
    
        # df = ti.readData(fileName)
        # df["Date"] = pd.to_datetime(df["Date"])
        # df = df.sort_values("Date", ascending=True)
        # print(df.head(n=5))
        
        # if purpose == "obv":
            # obv = ti.onBalanceVolume(df)
            # return json.dumps({"onBalanceVolume":obv})
        # return json.dumps({"Status":"API is working perfectly"})
    # else:
        # return json.dumps({"Status":"Please specify the parameters correctly"})


@app.route('/welcome')
def welcome():
    return '<h1>Welcome to MUST (https://must.co.in/)</h1>'
    
port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port), debug=True)
