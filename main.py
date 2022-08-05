import telebot
import time
import google_sheet

conf = []

with open("conf.txt", "r") as f:
    conf = f.read().split("~")
    # print(conf)
    assert len(conf) == 3

connector_sheet = google_sheet.googleSheet(conf[1],conf[2])
print(connector_sheet.get_dates())

# print(connector_sheet.make_time_record("15.08.2022\n(понедельник)", "123123", ["FIO", "class", "for", "id", "phone"]))

print(connector_sheet.get_my_record("id"))
p = conf[0]

