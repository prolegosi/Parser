import os
from backend import keep_alive
import telebot
import time
from settings import TG_TOKEN
import pendulum

bot = telebot.TeleBot(TG_TOKEN)


def create_graph():
  days = pendulum.now('Europe/Moscow').format('YYYY-MM-DD')

  """url = 'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=USD&to_symbol=RUB&apikey=W284OCJ6Y1UZJK7P'
  r = requests.get(url)
  data = r.json()
  r.close()"""
  print(days)






"""
@bot.message_handler(content_types=['text'])
def get_text_message(message):
  bot.send_message(message.from_user.id,message.text)
# echo-функция, которая отвечает на любое текстовое сообщение таким же текстом

keep_alive()#запускаем flask-сервер в отдельном потоке. Подробнее ниже...
bot.polling(non_stop=True, interval=0) #запуск бота"""
create_graph()