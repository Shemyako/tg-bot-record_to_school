import gspread

class googleSheet():
    # Конструктор. Получает имя файла, в котором токены и ссылку на google sheet
    def __init__(self, Filename:str, Tablename:str, ):
        self.__filename = Filename
        self.__tablename = Tablename
        self.__update
        self.__gc = gspread.service_account(self.filename)
        
    # Обновление данных их google sheet по ссылке
    def __update(self):
        self.__sh = __gc.open_by_url(self.tablename)
        self.__values = print(__sh.sheet1.get_all_values())



