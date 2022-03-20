import telebot
import requests
import time
from bs4 import BeautifulSoup
token = "5289266152:AAGWms-L_npYxGTmN_EaARLepZ3XTChfFg8"
id_channel = "@news_about_e"
bot = telebot.TeleBot(token)


@bot.message_handler(content_types=["text"])
def commands(message):
    back_post_time = open("id.txt").read()
    while True:
        post_text = parser(back_post_time)
        back_post_time = post_text[0:5]
        if post_text[0] != None:
            bot.send_message(id_channel, post_text)
            time.sleep(10) #время задержки между высыланием новостей


def parser(back_post_time):
    url = "https://www.ixbt.com/news/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    post_time = soup.find_all("span", class_="time_iteration_icon_light")[3].text
    if post_time != back_post_time:
        f = open("id.txt", "w")
        f.write(post_time)
        f.close()
        post = soup.find_all("li", class_="item")[3].text.strip()
        link = soup.find_all("li", class_="item")[3].find_all("a", href=True)[0].get('href')

        return f"{post_time}{post}{'https://ixbt.com'+link}", post_time
    else:
        return None, post_time


bot.polling()
