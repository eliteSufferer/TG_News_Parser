import asyncio
import datetime
import json

from aiogram import Bot, Dispatcher, executor, types
from config import token, user_id
from aiogram.utils.markdown import hbold, hunderline, hitalic, hlink
from vk_parser import check_news_update
from aiogram.dispatcher.filters import Text
bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["Все новости", "Последние 5 новостей", "Свежие новости"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer("Лента новостей", reply_markup=keyboard)


@dp.message_handler(Text(equals="Все новости"))
async def get_all_news(message: types.Message):
    with open("news_dict.json") as file:
        news_dict = json.load(file)
    for k, v in sorted(news_dict.items()):
        news = f"{hbold(datetime.datetime.fromtimestamp(v['article_date_timestamp']))}\n" \
               f"{hunderline(v['article_title'])} \n" \
               f"{hitalic(v['article_desc'])}\n" \
               f"{hlink('Читать далее...', v['article_url'])}"
        await message.answer(news)


@dp.message_handler(Text(equals="Последние 5 новостей"))
async def get_latest_news(message: types.Message):
    with open("news_dict.json") as file:
        news_dict = json.load(file)
    for k, v in sorted(news_dict.items())[-5:]:
        news = f"{hbold(datetime.datetime.fromtimestamp(v['article_date_timestamp']))}\n" \
               f"{hlink('Читать дальше...', v['article_url'])}"
        await message.answer(news)


@dp.message_handler(Text(equals="Свежие новости"))
async def get_fresh_news(message: types.Message):
    fresh_news = check_news_update()
    if len(fresh_news) >= 1:
        for k, v in sorted(fresh_news.items())[-5:]:
            news = f"{hbold(datetime.datetime.fromtimestamp(v['article_date_timestamp']))}\n" \
                   f"{hlink('Читать дальше...', v['article_url'])}"
            await message.answer(news)
    else:
        await message.answer("Пока свежих новостей нет")


async def news_per_time():
    while True:
        fresh_news = check_news_update()
        if len(fresh_news) >= 1:
            for k, v in sorted(fresh_news.items())[-5:]:
                news = f"{hbold(datetime.datetime.fromtimestamp(v['article_date_timestamp']))}\n" \
                       f"{hlink('Читать дальше...', v['article_url'])}"
                await bot.send_message(user_id, news)
        else:
            await bot.send_message(user_id, "Пока свежих новостей нет", disable_notification=True)
            # continue
        await asyncio.sleep(1800)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(news_per_time())
    executor.start_polling(dp)
