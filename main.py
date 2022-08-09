import telebot
import google_sheet

conf = []

# Читаем конфигурацию
with open("conf.txt", "r") as f:
    conf = f.read().split("~")
    # print(conf)
    assert len(conf) == 3

# Словарь с данными о записями
# [id] = {"date":.., "fio":.., "reason":.., "phone"}
statuses = {}

# Создаём объект для связи с гугл таблицей
connector_sheet = google_sheet.googleSheet(conf[1],conf[2])

# Создаё  объект для тг бота
p = conf[0]
bot = telebot.TeleBot(p, threaded=False)


# Выбор сотрудника для записи
@bot.message_handler(commands=['start'])
def first(message):
    # Удаляем из словаря если есть запись
    if message.from_user.id in statuses:
        del statuses[message.from_user.id]
    
    # Создаём клавиатуру с персоналом для записи
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Секретарь по учебной части', callback_data = 'start'))
    
    # Отправляем сообщение с клавиатурой
    bot.send_message(message.chat.id, 
    'Приветствую! Вы можете записаться в отделы, которые указаны ниже. Чтобы посмотреть запись' + 
    ' в конкретный раздел, нажмите на него, а после выберите "Посмотреть записи"\nЕсли Вам нужно,' + 
    ' чтобы это сообщение появилось ещё раз, введите /start', 
    reply_markup=markup)


# Меню с секретарём по учебной части
@bot.callback_query_handler(func=lambda call: call.data == 'start')
def start_callback_handler(call):
    # Создаём клавиутуру Запись/Мои записи и текст
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("Записаться", callback_data="start_record"), 
                telebot.types.InlineKeyboardButton("Мои записи", callback_data="my_records"))
    new_text = "Приветствую! Вы можете записаться на приём в этом боте. Для записи и просмотра Ваших записей использвуйте кнопки ниже. Чтобы вернуться в самое начало, нажмите на /start"
    
    # Изменяем сообщение на новое (с данными выше)
    bot.edit_message_text(text = new_text, 
                            chat_id = call.message.chat.id, 
                            message_id = call.message.message_id, 
                            reply_markup = markup)


# Мои записи
@bot.callback_query_handler(func=lambda call: call.data == 'my_records')
def my_records_callback_handler(call):
    # Получаем записи
    records = connector_sheet.get_my_record(call.from_user.id)
    # Создаём клавиатуру
    markup = telebot.types.InlineKeyboardMarkup()

    # Добавляем в клавиатуру кнопки с моими записями
    # Нажатием по ним отменяем записи потом
    for i in range(0, len(records)-1, 2):
        markup.add(telebot.types.InlineKeyboardButton(records[i], callback_data = "decline_"+str(records[i+1])))
    
    # Кнопка Назад
    markup.add(telebot.types.InlineKeyboardButton("Назад", callback_data = "start"))
    
    # Изменяем сообщение с данными выше
    new_text = "Чтобы отменить, нажмите на запись. Ваши записи:"
    bot.edit_message_text(text = new_text,
                            chat_id = call.message.chat.id, 
                            message_id = call.message.message_id, 
                            reply_markup = markup)


# Отмена записи после нажатия кнопки
@bot.callback_query_handler(func=lambda call: call.data[0:8] == "decline_")
def decline_record_callback_handler(call):
    # Пытаемся удалить запись
    answer = connector_sheet.decline_record(call.from_user.id ,call.data[8:len(call.data)])
    
    if (answer == 0): # Если ошибка
        bot.answer_callback_query(callback_query_id=call.id, text='Ошибка')
    else: # Если всё норм
        bot.answer_callback_query(call.id, text = "Готово!")

    # Обновляем список с записями
    my_records_callback_handler(call)


# Начало записи
@bot.callback_query_handler(func=lambda call: call.data == "start_record")
def start_record_query_handler(call):
    # Содаём запись в словаре
    statuses[call.from_user.id] = {}

    # Просим ввести ФИО
    new_text = "Введите *ФИО ребёнка* и отправьте их боту.\nЕсли в какой-то момент Вы совершите опечатку, введите /start и повторите всё заново"
    bot.edit_message_text(text = new_text, 
                            chat_id = call.message.chat.id, 
                            message_id = call.message.message_id,
                            parse_mode = "Markdown")


# Ввод ФИО
@bot.message_handler(func=lambda message: message.from_user.id in statuses and statuses[message.from_user.id] == {}, 
                        content_types = ['text'])
def fio_text_handler(message):
    # Проверка на вводимое ФИО
    if len(message.text) > 50:
        bot.send_message(message.from_user.id, "Введите меньше 50 символов")
        return 

    # Записываем в словарь введённые ФИО
    statuses[message.from_user.id]["fio"] = message.text
    
    # Просим ввести класс
    bot.send_message(message.from_user.id, 'Хорошо, теперь введите *класс ребёнка*', parse_mode = "Markdown")


# Ввод класса
@bot.message_handler(func=lambda message: (message.from_user.id in statuses and len(list(statuses[message.from_user.id])) == 1), 
                        content_types = ['text'])
def class_text_handler(message):
    # Смотрим длину вводимого класса
    if len(message.text) > 50:
        bot.send_message(message.from_user.id, "Введите меньше 50 символов")
        return 

    # Сохраняем введённый класс
    statuses[message.from_user.id]["class"] = message.text
    
    # Просим ввести причину
    bot.send_message(message.from_user.id, 'Хорошо,' + 
        'теперь введите *причину посещения* (подача документов, выдача документов, ' + 
        'выдача аттестатов, справки...). Итак, какая причина?', parse_mode = "Markdown")


# Ввод причины посещения
@bot.message_handler(func=lambda message: message.from_user.id in statuses and len(list(statuses[message.from_user.id])) == 2, 
                        content_types = ['text'])
def reason_text_handler(message):
    # Смотрим длину причины
    if len(message.text) > 50:
        bot.send_message(message.from_user.id, "Введите меньше 50 символов")
        return 

    # Сохраняем причину
    statuses[message.from_user.id]["reason"] = message.text
    
    # Блок если просить через кнопки номер телефона
    # markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    # markup.add(telebot.types.KeyboardButton("Поделиться номером", request_contact = True))

    # Просим ввести номер телефона
    bot.send_message(message.from_user.id, 'Отлично, почти закончили! ' + 
        'Теперь введите *номер телефона*', parse_mode = "Markdown") # , reply_markup=markup)


# Получение номера телефона
@bot.message_handler(func=lambda message: message.from_user.id in statuses and len(list(statuses[message.from_user.id])) == 3,
                        content_types = ['text'])
def contact_text_handler(message):
    # Длина номера больше 12 символов
    if len(message.text) > 12 or len(message.text) < 10:
        bot.send_message(message.from_user.id, 'При вводе возникла ошибка. Проверьте номер телефона и напишите его заново', 
                            parse_mode = "Markdown")
        return
    
    # Сохраняем номер
    statuses[message.from_user.id]["phone"] = message.text
    
    # Отправляем даты для записи
    send_dates(message)


# Отправка клавиатуры с датами
def send_dates(message, is_inline = False):
    # Даты, доступные для записи
    dates = connector_sheet.get_dates()

    # Если дат нет, извещаем об этом
    if len(dates) == 0:
        del statuses[message.from_user.id]
        bot.send_message(message.from_user.id, "Видимо, нет дат для записи. Обратитесь к администратору за подробной информацией\n/start")
        return

    # Создание клавиатуры
    markup = telebot.types.InlineKeyboardMarkup()
    for i in dates:
        markup.add(telebot.types.InlineKeyboardButton(i, callback_data="record_date_" + i))
    
    # Если нужно изменить клавиатуру, то меняем
    # Просим выбрать дату
    if is_inline:
        bot.edit_message_text(text = "Выберите дату", 
                            chat_id = call.message.chat.id, 
                            message_id = call.message.message_id, 
                            reply_markup = markup)
    else:
        bot.send_message(message.from_user.id, "Выберите дату", reply_markup=markup)


# Обработка выбора даты. Предлагаем время
@bot.callback_query_handler(func=lambda call: call.data[0:12] == "record_date_" 
                                            and call.from_user.id in statuses 
                                            and len(list(statuses[call.from_user.id])) == 4)
def record_date_callback_handler(call):
    # Получаем возможное время для записи
    times = connector_sheet.make_date_record(call.data[12:len(call.data)])
    
    # Если нет времени, говорим об этом
    if times == 0:
        bot.answer_callback_query(call.id, "Недоступно")
        # И выводим даты
        send_dates(call)
        return

    # Запоминаем ранее выбранную дату
    statuses[call.from_user.id]["date"] = call.data[12:len(call.data)]

    # Отправляем время для выбранной даты
    send_times(call, times)


# Отправка времени
def send_times(call, times = None):
    # Получаем множество времени для даты,
    # Если это множество не передали
    if times is None:
        times = connector_sheet.make_date_record(statuses[call.from_user.id]["date"])
    
    # Создаём клавиатуру с временами
    markup = telebot.types.InlineKeyboardMarkup()
    for i in range(0, len(times)-1, 2):
        markup.add(telebot.types.InlineKeyboardButton(times[i], callback_data="record_time_" + times[i]))

    # Отправляем доступное время для выбора
    bot.edit_message_text(text = "Выберите время", 
                            chat_id = call.message.chat.id, 
                            message_id = call.message.message_id, 
                            reply_markup = markup)


# Обработка выбора времени. Создаём запись
@bot.callback_query_handler(func=lambda call: call.data[0:12] == "record_time_" 
                                            and call.from_user.id in statuses 
                                            and len(list(statuses[call.from_user.id])) == 5)
def record_time_callback_handler(call):
    # Пытаемся создать запись
    short = statuses[call.from_user.id]
    answer = connector_sheet.make_time_record(short["date"], call.data[12:len(call.data)], 
        [short["fio"], short["class"], short["reason"], short["phone"], call.from_user.id])
    
    if answer == 1: # Всё норм
        # Извещаем, очищаем словарь, сообщение из самого начала
        bot.answer_callback_query(call.id, "Готово!")
        del statuses[call.from_user.id]
        start_callback_handler(call)
    elif answer == -1: # Время недоступно
        # Извещаем, отпарвляем доступное время
        bot.answer_callback_query(call.id, "Время недоступно!")
        send_times(call)
    elif answer == 0: # Дата недоступна
        # Извещаем, удаляем выбранную дату, отправляем доступные даты
        bot.answer_callback_query(call.id, "Дата недоступна!")
        del statuses[call.from_user.id]["date"]
        send_dates(call, True)


# Обработка нажатия кнопки (если запись не начата)
@bot.callback_query_handler(func=lambda call: True)
def null_callback_handler(call):
    '''
    Отправим стартовое сообщение
    '''
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("Записаться", callback_data="start_record"), 
        telebot.types.InlineKeyboardButton("Мои записи", callback_data="my_records"))

    if call.from_user.id in statuses:
        del statuses[call.from_user.if]

    bot.send_message(call.from_user.id, "Произошла ошибка. Повторите, пожалуйста, попытку заново /start", reply_markup = markup)


# Обработка ввода текста (если запись не начата)
@bot.message_handler(content_types = ['text'])
def text_handler(message):
    # Проверим, нужно ли уже выбирать дату
    if message.from_user.id in statuses and len(statuses[message.from_user.id]) == 4:
        send_dates(message)
        return

    # Очищаем статус
    if message.from_user.id in statuses:
        del statuses[message.from_user.if]

    # Стартовое сообщение
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("Записаться", callback_data="start_record"), 
        telebot.types.InlineKeyboardButton("Мои записи", callback_data="my_records"))

    bot.send_message(message.from_user.id, "Произошла ошибка. Повторите, пожалуйста, попытку заново /start", reply_markup = markup)


bot.polling()#none_stop=True)