import os
from backend import keep_alive
import telebot
import time

bot = telebot.TeleBot('6004287659:AAE7V5crZGYC6k9EdK7i0QmRE1IEPPLnZIk')

@bot.message_handler(content_types=['text'])
def get_text_message(message):
  bot.send_message(message.from_user.id,message.text)
# echo-функция, которая отвечает на любое текстовое сообщение таким же текстом

keep_alive()#запускаем flask-сервер в отдельном потоке. Подробнее ниже...
bot.polling(non_stop=True, interval=0) #запуск бота