import json

from aiogram import Bot, Dispatcher, executor, types
from config import token

bot = Bot(token=token)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.reply("Hello")


@dp.message_handler(commands="all_news")
async def get_all_news(message: types.Message):
    with open("news_dict.json") as file:
        news_dict = json.load(file)
    for k, v in sorted(news_dict.items()):
        news = f"{v['post_time']}\n" \
               f"{v['text']} \n" \
               f"{'https://ixbt.com/'+v['link']}"
        await message.answer(news)

if __name__ == "__main__":
    executor.start_polling(dp)
