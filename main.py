import telebot
import time
import google_sheet

conf = []

with open("conf.txt", "r") as f:
    conf = f.read().split("~")
    # print(conf)
    assert len(conf) == 3

connector_sheet = google_sheet.googleSheet(conf[1],conf[2])
p = conf[0]

bot = telebot.TeleBot(p, threaded=False)

@bot.message_handler(commands=['start'])
def first(message):
    if advertisment[1] > 0:
        bot.send_message(message.chat.id, advertisment[0])
        advertisment[1] = advertisment[1]-1
    bot.send_message(message.chat.id, '|Вы можете найти новую комнату или подать жалобу на неактивного пользователя или просто злодея. Для того, что бы у Вас снова появились данные клавиши, введите /start \n|/board \n|Сейчас в рулетке '+str(len(door)-door.count('')-1) +' собеседников.', reply_markup=keyboard1)


