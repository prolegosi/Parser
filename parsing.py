import requests
import pickle
import sqlite3
import sklearn

# открываем данные для стандартизации данных
m_m_open = open('files/min_max.txt', 'r')
val = m_m_open.read()
m_m_open.close()
min_max_lst = list(map(float, val.split()))

#Загружаем обученную модель

with open('files/USD_RUB_model.pkl', 'rb') as file:
    model = pickle.load(file)
file.close()
print(model)

url = 'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=USD&to_symbol=RUB&apikey=W284OCJ6Y1UZJK7P'
r = requests.get(url)
data = r.json()
r.close()
