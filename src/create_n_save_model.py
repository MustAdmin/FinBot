# -*- coding: utf-8 -*-

import os
import sys
import numpy as np
import pandas as pd
from fbprophet import Prophet
from sklearn.externals import joblib
import pickle


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
from src.mongoConnection import IgniteDBUtils as idu


def create_n_save_model():
    data = pd.read_csv(str(os.path.join(data_path, "INFY.csv")))[["Date", "ClosePrice"]]
    data = data.rename(columns={"Date":"ds", "ClosePrice":"y"})
    model = Prophet()
    # start creating model
    try:
        # instantiate Prophet
        model.fit(train) # fit the model with your dataframe
    except Exception as e:
        print("Error in model creation\n")
        print("Error Type: {}".format(type(e).__name__))
        print("Error description: {}".format(type(e).__doc__))
        sys.exit(0)
        
    # save model file
    try:
        with open("prophet_model.sav", "wb") as modl_file:
            pickle.dump(model, modl_file)
    except FileNotFoundError:
        print("Path not found to save the model!")
        sys.exit(0)
        
    return None