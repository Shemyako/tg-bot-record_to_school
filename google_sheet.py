import gspread


class googleSheet():
    '''
    table:
    date|time|fio|class|reason|phone|tg_id
    '''
    
    # Конструктор. Получает имя файла, в котором токены и ссылку на google sheet
    def __init__(self, Filename:str, Tablename:str, ):
        self.__filename = Filename
        self.__tablename = Tablename
        # Открытие токена
        self.__gc = gspread.service_account(self.__filename)
        # Получаем данные из гугл таблицы
        # self.__get_values()
        

    # Обновление данных их google sheet по ссылке
    def __get_values(func):
        # print(func)
        def decorated_get_values(self, *args):
            self.__sh = self.__gc.open_by_url(self.__tablename)
            # Список списков со всеми строками из гугл таблицы
            self.__values = self.__sh.sheet1.get_all_values()
            # Обрабатываем полученные данные
            self.__form_dates()
            return func(self, *args)
        return decorated_get_values


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
                act_date = i[0].replace('\n', ' ')
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
    @__get_values
    def get_dates(self):
        # print(2)
        return self.__dates


    # Смотрим возможность записи на какую-то дату
    @__get_values
    def make_date_record(self, date:str):
        '''
        На вход дату для получения возможного времени
        На выход:
        0 -> Нельзя на дату записаться

        '''
        # print(self.__dates)
        if date not in self.__dates:
            return 0

        return self.__dates[date]
    

    # Пытаемся записаться на какое-то время какого-то дня
    @__get_values
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

        # print(time)
        # print(self.__dates[date])
        # Если на это время записаться нельзя
        if (time not in self.__dates[date]):
            return -1

        if (len(data) != 5):
            return None

        # Находим индекс номера строки выбранного времени
        index = self.__dates[date].index(time) + 1

        # # Обновляем кэш
        # a = int(self.__dates[date][index]) - 1
        # # print(a)
        # self.__values[a][2:7] = data

        # Изменяем таблицу
        self.__make_record(self.__dates[date][index], data)

        # # Если больше свободного времени нет в таблице, удаляем это время
        # if (len(self.__dates[date]) == 2):
        #     del self.__dates[date]
        #     return 1

        # # Удаляем из кэша запись
        # del self.__dates[date][index-1]
        # del self.__dates[date][index-1]

        return 1

    
    # Изменяем данные в таблице (записываем человека)
    def __make_record(self, row, data):
        self.__sh.sheet1.update('C%s:G%s' % (row, row), [data])


    # Получить все записи пользователя
    @__get_values
    def get_my_record(self, tg_id):
        tg_id = str(tg_id)
        cur_day = ""
        counter = 0
        answer = []

        # Ищем записи с tg_id пользователя во всех записях
        for i in self.__values:
            counter += 1

            # Ставим текущую дату
            if i[0] != "":
                cur_day = i[0]
            
            if i[6] == tg_id:
                answer.append(cur_day + " " + i[1])
                answer.append(str(counter))
                
        return answer

    # Отмена записи
    def decline_record(self, tg_id, row):
        tg_id = str(tg_id)
        
        # Получаем мои записи
        records = self.get_my_record(tg_id)

        # Ищем в них ту, в которой строка нужная
        for i in range(0, len(records)-1, 2):
            if (records[i+1] == row):
                # Удаляем
                self.__make_record(row, ['','','','',''])
                return 1

        # Не получилось найти
        return 0        

