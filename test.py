import json

with open("news_dict.json") as file:
    news_dict = json.load(file)
ctime = "18:19"

if ctime in news_dict:
    print("уже есть")
else:
    print("добавляем")