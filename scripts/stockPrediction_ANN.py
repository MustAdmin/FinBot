import os
import sys
import re
import numpy as np 
from configparser import RawConfigParser
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.neural_network import MLPRegressor

#-------- define paths -----------#
basePath = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) # project root directory
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
testDataSize = config.getfloat('buildModel', 'testDataSize')

dataFile = os.path.join(dataPath, "testData.csv")
print(dataFile)
with open(dataFile) as f:
    csvData = f.read().split('\n')
    del csvData[0] # removes the header
    csvData = list(map(float, csvData))
    print(len(csvData))

rows = []
for g in range(int(len(csvData)/windowSize)):
    temp = []
    for j in range(5*g, 5*g+windowSize):
        temp.append(csvData[j])
    rows.append(temp)
rows = np.array(rows)
# print(rows)

feature = rows[:, 0:4] # every set of first four values will be taken as feature vector
target = rows[:, 4] # every fifth value will be taken as target/response

# #-------- data partitioning ----------#
featureTrain, featureTest, targetTrain, targetTest = train_test_split(feature, target, test_size=testDataSize)

# #-------- data scaling ----------#
minMaxScalar = MinMaxScaler(feature_range=(0, 1))
scaledFeatureTrain = minMaxScalar.fit_transform(featureTrain)
scaledFeatureTest = minMaxScalar.fit_transform(featureTest)
scaledTargetTrain = minMaxScalar.fit_transform(targetTrain)
scaledTargetTest = minMaxScalar.fit_transform(targetTest)

# #-------- defining the neuralnet ----------#
mlp_regressor = MLPRegressor(hidden_layer_sizes=(4, 4, 4), activation="logistic", solver='sgd', learning_rate="constant", learning_rate_init=0.003, random_state=99)

model = mlp_regressor.fit(scaledFeatureTrain, scaledTargetTrain)
pred = mlp_regressor.predict(scaledFeatureTest)

# print('\nPredicted values:\n{}'.format(pred))
# print('\nActual values:\n{}'.format(targetTest))

mape = 100 * np.sum(np.abs(scaledTargetTest - pred))/len(pred)
print('\nMAPE:\n{}\n\n'.format(mape))