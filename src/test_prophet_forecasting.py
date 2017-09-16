# -*- coding: utf-8 -*- 
import pandas as pd
from fbprophet import Prophet
import numpy as np
import matplotlib.pyplot as plt
import datetime
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from math import sqrt

plt.rcParams['figure.figsize']=(20,10)
plt.style.use('ggplot')

def prep_data():
    df_data = pd.read_csv("Your/CSV/data_path/my_data_file.csv", usecols=['ds', 'y'], low_memory=False)
  
    df_data =  df_data.reset_index(drop=True) #FIXME: not needed if indeces are in continuous sequence
    df_data['ds'] =pd.to_datetime(df_data.ds)
    df_data.index = df_data['ds']
    df_data =  df_data.sort_index()

    df_data_weekly = df_data.groupby(pd.TimeGrouper(freq='W')).count()
    df_data_weekly['ds'] = df_data_weekly.index
    df_data_weekly.to_csv('Your/file/save/path/df_data_weekly.csv')

    N = 25 #FIXME: last N-weeks data will be used for performance measure
    train, test = df_data_weekly.iloc[0:-N,:], df_data_weekly.iloc[-N:,:]
    #print(test.head())
    #df_data_weekly['y'].plot()
    #plt.show()
    return(train, test, N)
    
def decompose(train, future_periods):    
    train['y_orig'] = train['y'] # to save a copy of the original data..you'll see why shortly. 
    # log-transform y
    train['y'] = np.log(train['y'])
    #print(complaints_df_train.head())

    model = Prophet() #instantiate Prophet
    model.fit(train) #fit the model with your dataframe

    #Now its time to start forecasting. 
    future_data = model.make_future_dataframe(periods=future_periods, freq ='w') #FIXME
    forecast_data = model.predict(future_data)
    #print(forecast_data[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
    model.plot(forecast_data)
    #plt.show()
    model.plot_components(forecast_data)
    plt.show()
    #forecast_data.index = forecast_data.ds
    return(forecast_data)

def evaluate(forecast_data, test, future_periods, train):
    df_complaints = pd.concat([train, test])
    #print("df_complaints:", df_complaints)

    fig, ax1 = plt.subplots()
    df_complaints['y'].plot(x=ax1)
    #plt.show()

    forecast_mask = forecast_data.iloc[-future_periods:, :]
    #print("forecast_mask:", forecast_mask)
    y_forecasted = np.exp(forecast_mask.yhat).round()
    y_forecasted = y_forecasted.tolist()
    forecast_yhat_upper = np.exp(forecast_mask.yhat_upper).round()
    forecast_yhat_upper = forecast_yhat_upper.tolist()
    forecast_yhat_lower = np.exp(forecast_mask.yhat_lower).round()
    forecast_yhat_lower = forecast_yhat_lower.tolist()
    
    y_truth = test.iloc[:,0].values
    y_orig = train.iloc[:, 0].values
    y_orig = y_orig.tolist()
    y_total = y_orig + y_forecasted
    y_total = pd.DataFrame(y_total, columns=['y'])
    y_total.index = df_complaints['ds']
    print("y_total:", y_total)
    print("Projected_Sales_Number:", y_forecasted)
    print("Actual_Sales_Count:", y_truth)

    mse = mean_squared_error(y_truth, y_forecasted)
    rmse = sqrt(mse)
    print('RMSE: %.3f' % rmse)
    MAPE = np.mean(np.abs((y_truth - y_forecasted) / y_truth)) * 100
    print("MAPE:", MAPE)

    #---------------------------------
    # Now...plot everything
    #---------------------------------    
    y_total['y'].plot(x=ax1, linestyle=':', linewidth = 2.0, color = 'blue') 
    #ax1 = y_total['y'].plot(linestyle=':')
    ax1.fill_between(forecast_mask.index, forecast_yhat_upper, forecast_yhat_lower, alpha=0.5, color='darkgray')
    ax1.set_title('Bank account or service: actual-complaints (continuous-line) vs complaints-forecast (blue-dotted-line)')
    ax1.set_ylabel('Weekly-Complaints-Count')
    ax1.set_xlabel('Year')
    plt.show()

if __name__ == "__main__": 
    (train,  test, future_periods) = prep_data()
    train_copy = train.copy(deep=True)
    forecast_data = decompose(train, future_periods)
    evaluate(forecast_data, test, future_periods, train_copy)
