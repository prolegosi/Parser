import requests
import pickle
import sqlite3
import sklearn
import numpy as np


def completion():
    pass


con = sqlite3.connect('data.db')
cur = con.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS USD_RUB_data(
        date TEXT PRIMARY KEY,
        open REAL,
        high REAL,
        low REAL,
        close REAL
        close_c REAL
        predict REAL);
    """)

# открываем данные для стандартизации данных
m_m_open = open('files/min_max.txt', 'r')
val = m_m_open.read()
m_m_open.close()
min_max_lst = list(map(float, val.split()))

# Загружаем обученную модель
with open('files/USD_RUB_model.pkl', 'rb') as file:
    model = pickle.load(file)
file.close()

url = 'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=USD&to_symbol=RUB&apikey=W284OCJ6Y1UZJK7P'
r = requests.get(url)
data = r.json()
r.close()

counter = 0
# Обработка полученных данных и занесение их в базу данных
for i in data['Time Series FX (Daily)'].items():
    d = dict(i[1])
    date = i[0]
    lst = []

    for j in d.items():
        lst.append(float(j[1]))

    close_c = lst[3]

    lst = [(x - min_max_lst[0]) / (min_max_lst[1] - min_max_lst[0]) for x in lst]
    opening, high, low, close = tuple(lst)
    """X = np.array(lst).reshape(1, -1)
    print(X)
    if counter > 0:
        predict = model.predict(X)
    else
    print(predict, close_c)"""
    try:
        cur.execute(f"""INSERT INTO USD_RUB_data VALUES('{date}',{opening},{high},{low}, {close}, {close_c}) """)
    except sqlite3.IntegrityError:
        print('дата уже существует')
    counter += 1
