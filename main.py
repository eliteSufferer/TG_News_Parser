import telebot
import requests
import time

from bs4 import BeautifulSoup

token = "token"
id_channel = "@news_about_e"
bot = telebot.TeleBot(token)


@bot.message_handler(content_types=['text'])
def commands(message):
    # bot.send_message(channel_id, message.text)
    if message.text == "Старт":
        # bot.send_message(channel_id, "Hello")
        back_post_id = None
        while True:
            post_text = parser(back_post_id)
            back_post_id = post_text[1]

            if post_text[0] != None:
                bot.send_message(id_channel, post_text[0])
                time.sleep(10)
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши Старт")


def parser(back_post_id):
    URL = "https://habr.com/ru/search/?q=python&target_type=posts&order=relevance"

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    post = soup.find("article", class_="tm-articles-list__item", id=True)
    post_id = post["id.txt"]

    if post_id != back_post_id:
        title = post.find("h2", class_="tm-article-snippet__title tm-article-snippet__title_h2").text.strip()

        return f"{title}", post_id
    else:
        return None, post_id


bot.polling()
