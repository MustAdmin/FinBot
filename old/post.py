import requests

param = {}

#param['fileName'] = '500209.csv'
#param['purpose'] = 'obv'

param['x'] = '5'
param['y'] = '6'

r = requests.post("http://127.0.0.1:5000/test", data=param).content
print(r)