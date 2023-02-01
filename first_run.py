import requests
import pickle
import sqlite3
import pendulum
import numpy as np

con = sqlite3.connect('data.db')
cur = con.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS USD_RUB_data(
        days TEXT PRIMARY KEY,
        opening REAL,
        high REAL,
        low REAL,
        closes REAL,
        close_c REAL,
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
    lst = []
    for j in d.items():
        lst.append(float(j[1]))
    # Нормализация
    lst_norm = [(x - min_max_lst[0]) / (min_max_lst[1] - min_max_lst[0]) for x in lst]

    days = i[0]
    opening, high, low, closes = tuple(lst_norm)
    close_c = lst[3]
    X = np.array(lst_norm).reshape(1, -1)
    # Создание предсказания
    predict_after = model.predict(X)

    if counter > 0:
        predict = round(float(predict_before), 2)
    else:
        predict = close_c

    try:

        cur.execute(f"""INSERT INTO USD_RUB_data VALUES('{days}', {opening}, {high}, {low}, {closes}, {close_c}, {predict}) """)
    except sqlite3.IntegrityError:
        print('дата уже существует')

    predict_before = predict_after

    counter += 1

days = pendulum.tomorrow().format('YYYY-MM-DD')
cur.execute(f"""INSERT INTO USD_RUB_data (days, predict) VALUES('{days}',{round(float(predict_after), 2)}) """)

print('Данные созданы')
cur.close()

