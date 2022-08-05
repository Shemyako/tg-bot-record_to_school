import gspread
###
#   Сделать изменение кэша __value после записи
###



class googleSheet():
    # Конструктор. Получает имя файла, в котором токены и ссылку на google sheet
    def __init__(self, Filename:str, Tablename:str, ):
        self.__filename = Filename
        self.__tablename = Tablename
        # Открытие токена
        self.__gc = gspread.service_account(self.__filename)
        # Получаем данные из гугл таблицы
        self.__get_values()
        

    # Обновление данных их google sheet по ссылке
    def __get_values(self):
        self.__sh = self.__gc.open_by_url(self.__tablename)
        # Список списков со всеми строками из гугл таблицы
        self.__values = self.__sh.sheet1.get_all_values()
        # Обрабатываем полученные данные
        self.__form_dates()


    # Просматриваем данные из __get_values и формируем словарь с датами к записи
    def __form_dates(self):
        # Текущая дата
        act_date = ""
        # Счётчик для вычисления строки
        counter = 0
        # Обнуление словаря с временем
        self.__dates = {}

        for i in self.__values:
            counter += 1
            # Если дата есть, она - актуальная
            if (i[0] != ""):
                act_date = i[0]
                self.__dates[act_date] = []
            
            # Если поле с ФИО (i[2]) пустое, => запись возможна
            if (i[2] == "" and i[1] != ""):
                # Добавляем время и номер строки, что б потом было удобно редактировать таблицу
                self.__dates[act_date].append(i[1])
                self.__dates[act_date].append(counter)

        # Получаем все ключи из словаря
        keys = list(self.__dates)
        
        # Проходимся по ним и ищем даты без возможности записи, после удаляем их
        for key in keys:
            if len(self.__dates[key]) == 0:
                del self.__dates[key]


    # Получение дат, на которые можно соверщить запись
    def get_dates(self):
        return self.__dates
        # return list(self.__dates)


    # Смотрим возможность записи на какую-то дату
    def make_date_record(self, date:str):
        '''
        На вход дату для получения возможного времени
        На выход:
        0 -> Нельзя на дату записаться

        '''
        if date not in self.__dates:
            return 0

        return self.__dates[date][::2]
    

    # Пытаемся записаться на какое-то время какого-то дня
    def make_time_record(self, date:str, time:str, data:list):
        '''
        На вход дату и время для записи
        На выход:
        0 -> Нельзя на дату записаться
        1 -> Нельзя на время записаться
        '''
        # Если на эту дату больше нельзя записаться
        if (date not in self.__dates):
            return 0

        # Если на это время записаться нельзя
        if (time not in self.__dates[date]):
            return -1

        # Находим индекс номера строки выбранного времени
        index = self.__dates[date].index(time) + 1

        # Изменяем таблицу
        self.__make_record(self.__dates[date][index], data)

        # Удаляем из кэша запись
        del self.__dates[date][index-1]
        del self.__dates[date][index-1]
        # return self.__dates

    
    # Изменяем данные в таблице (записываем человека)
    def __make_record(self, row, data):
        self.__sh.sheet1.update('C%s:G%s' % (row, row), [data])


    # Получить все записи пользователя
    def get_my_record(self, tg_id):
        tg_id = str(tg_id)
        cur_day = ""
        counter = 0
        answer = []

        for i in self.__values:
            counter += 1

            if i[0] != "":
                cur_day = i[0]
            
            print(i)
            if i[5] == tg_id:
                answer.append(i[0] + " " + i[1])
                answer.append(counter)
        
        return answer



        







