import os
import sys
import json
import cherrypy
import numpy as np
import pandas as pd
from configparser import RawConfigParser
from finbotAnalytics import TechnicalIndicator

class finbotAnalyticsApi(object):
    @cherrypy.expose
    def GetTechIndicator(self, **kwargs):
        try:
            fileName = kwargs["fileName"].strip()
        except Exception:
            fileName = ""
        try:
            purpose = kwargs["purpose"].strip()
        except Exception:
            purpose = ""
        
        if fileName and purpose:
            ti = TechnicalIndicator()
        
            df = ti.readData(fileName)
            df["Date"] = pd.to_datetime(df["Date"])
            df = df.sort_values("Date", ascending=True)
            # print(df.head(n=5))
            
            if purpose == "obv":
                obv = ti.onBalanceVolume(df)
                return json.dumps({"onBalanceVolume":obv})
            return json.dumps({"Status":"API is working perfectly"})
        else:
            return json.dumps({"Status":"Please specify the parameters correctly"})
    
if __name__ == "__main__":
    cherrypy.server.socket_host = "127.0.0.1"
    cherrypy.server.socket_port = 8888
    cherrypy.quickstart(finbotAnalyticsApi())