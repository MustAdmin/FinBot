import requests

param = {}

param['fileName'] = '500209.csv'
param['purpose'] = 'obv'


r = requests.post("http://localhost:8888/GetTechIndicator", data=param).content
print(r)