from __future__ import print_function
import os
import sys
import re
import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from ConfigParser import RawConfigParser

#-------- define paths -----------#
basePath = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) # root directory 
dataPath = os.path.join(basePath, "data")
configPath = os.path.join(basePath, "config")
modelPath = os.path.join(basePath, "model")
scriptPath = os.path.dirname(__file__)

#-------- set basePath ----------#
os.chdir(basePath)
sys.path.append(basePath)

#-------- read configuration file ----------#
config = RawConfigParser()
config.read(os.path.join(configPath, 'config.ini'))
windowSize = config.getint('preProcess', 'windowSize')
# print(type(windowSize))

# print(os.path.dirname(__file__)) # directory name containing the script
# print(os.path.basename(__file__)) # current file name
# print(os.path.abspath(__file__)) # absolute path
# print(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
# print(os.path.dirname(os.path.realpath(__file__)))

dataFile = os.path.join(dataPath, 'testData.csv')
with open(dataFile) as f:
    csvData = f.read().split('\n')
    del csvData[0] # removes the header
    csvData = map(float, csvData)
    # print(csvData)

rows = []
for g in range(len(csvData)/windowSize):
    temp = []
    for j in range(5*g, 5*g+windowSize):
        temp.append(csvData[j])
    rows.append(temp)
rows = np.array(rows)
# print(rows)

cols = zip(*rows)
feature = np.array(zip(*cols[0:4])) # first four values are taken as features
target = np.array(cols[4]) # last value is taken as target

# print(target)

# print(target.shape)
# print(target)

#-------- data normalization ----------#
minMaxScalar = MinMaxScaler(feature_range=(0, 1))
normedFeature = minMaxScalar.fit_transform(feature)
normedTarget = minMaxScalar.fit_transform(target)

featureTrain, featureTest, targetTrain, targetTest = train_test_split(normedFeature, normedTarget, test_size=0.30)


mlp_regressor = MLPRegressor(hidden_layer_sizes=(4, 4), activation="logistic", solver='sgd', learning_rate="constant", learning_rate_init=0.003, random_state=99)

model = mlp_regressor.fit(featureTrain, targetTrain)
pred = mlp_regressor.predict(featureTest)

print('\nPredicted values:\n{}'.format(pred))
print('\nActual values:\n{}'.format(targetTest))

mape = 100 * np.sum(np.abs(targetTest - pred))/len(pred)
print('\nMAPE:\n{}'.format(mape))
