# -*- coding: utf-8 -*-

"""
@author: Koushik Khan [write2koushik.stat@outlook.com]
@copyright: MUST Research Club [www.must.co.in]
"""

import os
import sys
import json
import numpy as np
import pandas as pd
from fbprophet import Prophet
from flask import Flask, request
from collections import OrderedDict

# set path:-----------------------------------------
home = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
config_path = str(os.path.join(home, "config"))
data_path = str(os.path.join(home, "data"))
model_path = str(os.path.join(home, "model"))
print(model_path)

# append home:---------------------------------------
sys.path.append(home)
os.chdir(home)

# import custom modules:-----------------------------
from src.mongo_connection import DatabaseUtilities as idu

app = Flask(__name__)

@app.route('/finbot_forecasting_engine', methods=['POST'])
# Run Code: -------------------------------------------------------------------
def finbot_forecasting_engine():
    try:
        days_to_forecast = request.form['days_to_forecast']
    except:
        try:
            days_to_forecast = request.values['days_to_forecast']
        except:
            days_to_forecast = " "
    
    if days_to_forecast:
    
        # create db connection:------------------------------------------------------------------
        # conn_obj = idu(ipaddress, port, userid, paswd, dbName)   
        # db = conn_obj.ConnectDB()
        # data = conn_obj.PullData(collection_name, db)
        
        data = pd.read_csv(str(os.path.join(data_path, "IBM.csv")))[["Date", "Close"]]
        data = data.rename(columns={"Date":"ds", "Close":"y"})
        
        model = Prophet(daily_seasonality=True)
        model.fit(data)
        
        future_data = model.make_future_dataframe(periods=int(days_to_forecast)) #FIXME
        # print("debug-0:", future_data.shape)
        forecast_data = model.predict(future_data)
        # print("debug-1:", forecast_data.shape)

        future_ds = forecast_data.tail(int(days_to_forecast))["ds"].tolist()
        forecasted_values = forecast_data.tail(int(days_to_forecast))["yhat"].tolist()

        # creating formatted output
        forecastOutput = []
        for i in range(int(days_to_forecast)):
            info = OrderedDict()
            info[str(future_ds[i])] = forecasted_values[i]
            
            forecastOutput.append(info)

        result = dict()
        result["dateWiseForecast"] = forecastOutput
        result_in_json = json.dumps(result)
        
        return result_in_json
        
    else:
        return json.dumps({"Status":"Please specify all the parameters correctly!"})
        
        
if __name__ == "__main__":
    app.run()