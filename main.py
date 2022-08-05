import telebot
import time

conf = []

with open("conf.txt", "r") as f:
    conf = f.read().split("~")
    assert len(conf) != 3

p = conf[0]

bot = telebot.TeleBot(p, threaded=False)
#bot = telebot.TeleBot(p)
# Команты
door = ['q']

keyboard = telebot.types.ReplyKeyboardMarkup(True)
keyboard.row('/start')

keyboard1 = telebot.types.InlineKeyboardMarkup(row_width=2)
start_button = telebot.types.InlineKeyboardButton(text = 'Следующая комната', callback_data = '1')
start_button2 = telebot.types.InlineKeyboardButton(text = 'Жалоба', callback_data = '2')
keyboard1.add(start_button, start_button2)

#keyboard = telebot.types.ReplyKeyboardMarkup(True)
#keyboard.row('Найти комнату','Жалоба')
# Список для рекламы
advertisment = ['',0]

# Перезагрузка бота
@bot.message_handler(commands=['reload'])
def rere(message):
    if message.chat.id == 424184511 or message.chat.id == 785530778:
        for i in range(1,len(door)):
            if door[i]!='':
                bot.send_message(door[i], '|Чат рулетка будет перезагружена')


@bot.message_handler(commands=['start'])
def first(message):
    if advertisment[1] > 0:
        bot.send_message(message.chat.id, advertisment[0])
        advertisment[1] = advertisment[1]-1
    bot.send_message(message.chat.id, '|Вы можете найти новую комнату или подать жалобу на неактивного пользователя или просто злодея. Для того, что бы у Вас снова появились данные клавиши, введите /start \n|/board \n|Сейчас в рулетке '+str(len(door)-door.count('')-1) +' собеседников.', reply_markup=keyboard1)
    
    #print(message)

# Статистика бота (Онлайн людей)
@bot.message_handler(commands=['static'])
def first(message):
    bot.send_message(message.chat.id, '|Сейчас в чате '+str(len(door)-door.count('')-1) +' собеседников')
    #print(message)

# Показать клавиатуру c /start
@bot.message_handler(commands=['board'])
def keyb(message):
    bot.send_message(message.chat.id,'|Готово',reply_markup = keyboard)


# О фотках
@bot.message_handler(content_types=['photo'])
def photo(message):
    #bot.send_message(message.chat.id, '-------------------------------------------------------------------------------------')
    bot.send_message(message.chat.id, '|Эта рулетка не предназначена для фото. Используйте стикеры.')
    #bot.send_message(message.chat.id, '-------------------------------------------------------------------------------------')
    

# Добавить рекламу
# /pridor Текст сообщения|Количество раз показать
@bot.message_handler(commands=['pridor'])
def adv(message):
    if message.chat.id == 424184511 or message.chat.id == 785530778:
        global advertisment
        advertisment = message.text[8:len(message.text)].split('|')
        advertisment[1] = int(advertisment[1])


#Пересыл сообщений
@bot.message_handler(content_types=['text'])
def repeat(message):
    messagechatid = message.chat.id
    if door.count(messagechatid)==0:
        bot.send_message(messagechatid, '|Ты комнату сначала выбери /start')
        return
    #print(door)
    elif (door.index(messagechatid))%2 == 0:
        if door[door.index(messagechatid)-1]!='':
            bot.send_message( door[door.index(messagechatid)-1], message.text )
        else:
            #bot.send_message(messagechatid, '-------------------------------------------------------------------------------------')
            bot.send_message(messagechatid, '|Дождитесь собеседника')
            #bot.send_message(messagechatid, '-------------------------------------------------------------------------------------')
    else:
        if door[door.index(messagechatid)+1]!='':
            bot.send_message( door[door.index(messagechatid)+1], message.text )
        else:
            #bot.send_message(messagechatid, '-------------------------------------------------------------------------------------')
            bot.send_message(messagechatid, '|Дождитесь собеседника')
            #bot.send_message(messagechatid, '-------------------------------------------------------------------------------------')
        

#Пересыл стикеров
@bot.message_handler(content_types=['sticker'])
def stick(message):
    messagechatid = message.chat.id
    #print(message)
    if door.count(messagechatid)==0:
        bot.send_message(messagechatid, '|Ты комнату сначала выбери /start')
        return
    #print(door)
    elif (door.index(messagechatid))%2 == 0:
        if door[door.index(messagechatid)-1]!='':
            bot.send_sticker( door[door.index(messagechatid)-1], message.sticker.file_id )
        else:
            #bot.send_message(messagechatid, '-------------------------------------------------------------------------------------')
            bot.send_message(messagechatid, '|Дождитесь собеседника')
            #bot.send_message(messagechatid, '-------------------------------------------------------------------------------------')
    else:
        if door[door.index(messagechatid)-1]!='':
            bot.send_sticker( door[door.index(messagechatid)+1], message.sticker.file_id )
        else:
            #bot.send_message(messagechatid, '-------------------------------------------------------------------------------------')
            bot.send_message(messagechatid, '|Дождитесь собеседника')
            #bot.send_message(messagechatid, '-------------------------------------------------------------------------------------')

#Голосовухи
@bot.message_handler(content_types=['voice'])
def stick(message):
    messagechatid = message.chat.id
    #print(message)
    #bot.send_voice(messagechatid, message.voice.file_id )
    #print(message)
    if door.count(messagechatid)==0:
        bot.send_message(messagechatid, '|Ты комнату сначала выбери /start')
        return
    #print(door)
    elif (door.index(messagechatid))%2 == 0:
        if door[door.index(messagechatid)-1]!='':
            bot.send_voice( door[door.index(messagechatid)-1], message.voice.file_id )
        else:
            #bot.send_message(messagechatid, '-------------------------------------------------------------------------------------')
            bot.send_message(messagechatid, '|Дождитесь собеседника')
            #bot.send_message(messagechatid, '-------------------------------------------------------------------------------------')
    else:
        if door[door.index(messagechatid)-1]!='':
            bot.send_voice( door[door.index(messagechatid)+1], message.voice.file_id )
        else:
            #bot.send_message(messagechatid, '-------------------------------------------------------------------------------------')
            bot.send_message(messagechatid, '|Дождитесь собеседника')
            #bot.send_message(messagechatid, '-------------------------------------------------------------------------------------')


        
#Смена комнаты разная для нового и старого пользователей. Если комнат нет, создаются 2 новые
#Если пользователь переходит в другую комнату, старая = 'id'+'-'/ старая = 0()ноль
@bot.callback_query_handler(func = lambda call: True)
def admin(call):
    messagechatid = call.from_user.id
    #print(call.data)
    #print(messagechatid)
    if call.data == '1': #Поиск комнаты
        #print('22')
        if door.count(messagechatid) == 0: #Новый пользователь
            try:
                door.index('')
            except ValueError:
                door.append('')
                door.append('')
            door[door.index('')] = messagechatid
        else: #Смена комнаты
            
            #Строки ниже: извещение о сливе
            if (door.index(messagechatid))%2 == 0:
                if door[door.index(messagechatid)-1] != '':
                    #bot.send_message( door[door.index(messagechatid)-1], '-------------------------------------------------------------------------------------')
                    bot.send_message( door[door.index(messagechatid)-1], '|Ваш собеседник покинул комнату. Поменяйте комнату (/start) или ждите нового' )
                    #bot.send_message( door[door.index(messagechatid)-1], '-------------------------------------------------------------------------------------')
            else:
                if door[door.index(messagechatid)+1] != '':
                    #bot.send_message( door[door.index(messagechatid)+1], '-------------------------------------------------------------------------------------')
                    bot.send_message( door[door.index(messagechatid)+1], '|Ваш собеседник покинул комнату. Поменяйте комнату (/start) или ждите нового' )
                    #bot.send_message( door[door.index(messagechatid)+1], '-------------------------------------------------------------------------------------')
            door[door.index(messagechatid)] = 0
            #print(door)
            try:
                door.index('')
            except ValueError:
                door.append('')
                door.append('')
            door[door.index('')] = messagechatid
            door[door.index(0)] = ''
        #print(door)
        #bot.send_message(messagechatid, '-------------------------------------------------------------------------------------')
        bot.send_message(messagechatid, '|Комната найдена)')
        #bot.send_message(messagechatid, '-------------------------------------------------------------------------------------')
        #if (door.index(messagechatid)+1)/2 == int((door.index(messagechatid)+1)/2):
        #Сместил список на +1
        #print(door.index(messagechatid)%2)
        if (door.index(messagechatid))%2 == 0:
            if door[door.index(messagechatid)-1] == '':
                #bot.send_message( door[door.index(messagechatid)], 'Подождите пока появится собеседник или поменяйте комнату (/start)' )
                #bot.send_message(messagechatid, '-------------------------------------------------------------------------------------')
                bot.send_message(messagechatid, '|Подождите пока появится собеседник или поменяйте комнату (/start)' )
                #bot.send_message(messagechatid, '-------------------------------------------------------------------------------------')
            else:
                #bot.send_message( door[door.index(messagechatid)-1], '-------------------------------------------------------------------------------------')
                bot.send_message( door[door.index(messagechatid)-1], '|Извещение: в комнате появился собеседник')
                #bot.send_message( door[door.index(messagechatid)-1], '-------------------------------------------------------------------------------------')
        else:
            if door[door.index(messagechatid)+1] == '':
                #bot.send_message( messagechatid, '-------------------------------------------------------------------------------------')
                bot.send_message( messagechatid, '|Подождите пока появится собеседник или поменяйте комнату (/start)' )
                #bot.send_message( messagechatid, '-------------------------------------------------------------------------------------')
            else:
                #bot.send_message( door[door.index(messagechatid)+1], '-------------------------------------------------------------------------------------')
                bot.send_message( door[door.index(messagechatid)+1], '|Извещение: в комнате появился собеседник')
                #bot.send_message( door[door.index(messagechatid)+1], '-------------------------------------------------------------------------------------')
    #Жалоба
    elif call.data == '2':
        if door.count(messagechatid) == 0:
            bot.send_message((messagechatid), '|У Вас нет собеседника')            
        
        elif (door.index(messagechatid))%2 == 0:
            if door[door.index(messagechatid)-1] != '':
                bot.send_message( door[door.index(messagechatid)-1], '|Собеседник отказался от Вас. Ищите новую комнату с нормальным человеком', reply_markup=keyboard1)
                #bot.send_message((messagechatid), '----------------------------------------------------')
                bot.send_message((messagechatid), '|Можешь спать спокойно, я его кикнул')
                #bot.send_message((messagechatid), '----------------------------------------------------')
                door[door.index(messagechatid)-1] = ''
                print(door)
            else:
                bot.send_message((messagechatid), '|У Вас нет собеседника')
        else:
            if door[door.index(messagechatid)+1] != '':
                bot.send_message( door[door.index(messagechatid)+1], '|Собеседник отказался от Вас. Ищите новую комнату с нормальным человеком', reply_markup=keyboard1)
                #bot.send_message((messagechatid), '----------------------------------------------------')
                bot.send_message((messagechatid), '|Можешь спать спокойно, я его кикнул')
                #bot.send_message((messagechatid), '----------------------------------------------------')
                door[door.index(messagechatid)+1] = ''
                print(door)
            else:
                bot.send_message((messagechatid), '|У Вас нет собеседника')
        
            
while True:
    try:
        bot.polling(none_stop=True)

    except Exception:
        time.sleep(3)
        
