import os
from backend import keep_alive
import telebot
import time
from settings import TG_TOKEN
import pendulum
import sqlite3
import requests
import numpy as np
import pickle
import matplotlib as plt

bot = telebot.TeleBot(TG_TOKEN)
with open('files/USD_RUB_model.pkl', 'rb') as file:
    model = pickle.load(file)
file.close()

def create_graph():
    now = pendulum.now('Europe/Moscow').format('YYYY-MM-DD')

    con = sqlite3.connect('data.db')
    cur = con.cursor()

    cur.execute(""" SELECT MAX(days) FROM USD_RUB_data""")
    row = cur.fetchall()
    db_date = row[0][0]

    print(now, db_date)
    if now > db_date:
    # открываем данные для нормализации
        m_m_open = open('files/min_max.txt', 'r')
        val = m_m_open.read()
        m_m_open.close()
        min_max_lst = list(map(float, val.split()))

    # получаем данные с API
        url = 'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=USD&to_symbol=RUB&apikey=W284OCJ6Y1UZJK7P'
        r = requests.get(url)
        data = r.json()

        counter = 0
        for i in data['Time Series FX (Daily)'].items():
            done = True
            d = dict(i[1])
            lst = []
            if db_date > now:
                # написать ретурн
                break
            for j in d.items():
                lst.append(float(j[1]))
            # Нормализация
            lst_norm = [(x - min_max_lst[0]) / (min_max_lst[1] - min_max_lst[0]) for x in lst]

            days = i[0]
            # если даты нет в базе продолжаем
            if days == db_date:
                done = False
            opening, high, low, closes = tuple(lst_norm)
            close_c = lst[3]
            X = np.array(lst_norm).reshape(1, -1)
            # Создание предсказания
            predict_after = model.predict(X)

            if counter > 0:
                predict = round(float(predict_before), 2)
            else:
                cur.execute(f""" SELECT predict FROM USD_RUB_data WHERE days = '{db_date}'""")
                pred = cur.fetchall()
                predict = pred[0][0]

            if not done:
                try:

                    cur.execute(f"""INSERT INTO USD_RUB_data VALUES('{days}', {opening}, {high}, {low}, {closes}, {close_c}, {predict}) """)
                except sqlite3.IntegrityError:
                    print('дата уже существует')

            predict_before = predict_after
            if not done:

                break
            counter += 1
        days = pendulum.tomorrow().format('YYYY-MM-DD')


        cur.execute(f"""INSERT INTO USD_RUB_data (days, predict) VALUES('{days}',{round(float(predict_after), 2)}) """)

        # Получаем данные ля графика


        # строим график и сохраняем.
        plt.plot(real)
        plt.plot(pred)
        plt.savefig('files/predict_show.jpg')

    con.commit()

    cur.close()


"""
@bot.message_handler(content_types=['text'])
def get_text_message(message):
  bot.send_message(message.from_user.id,message.text)
# echo-функция, которая отвечает на любое текстовое сообщение таким же текстом

keep_alive()#запускаем flask-сервер в отдельном потоке. Подробнее ниже...
bot.polling(non_stop=True, interval=0) #запуск бота"""
create_graph()
