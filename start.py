import asyncio
import os

import aiomysql
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from dotenv import load_dotenv, find_dotenv
from info import Admin
from main import algorithm, print_form_form


load_dotenv(find_dotenv())
bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()



@dp.callback_query(StateFilter(None), lambda c: c.data and c.data.startswith('btn_1_'))
async def get_tel(callback_query: types.CallbackQuery, message: types.Message, state: FSMContext):
    index = int(callback_query.data.split("_")[-1])





async def main():
    # dp.startup.register(start_message)
    # dp.shutdown.register(end_message)
    connection_pool = await aiomysql.create_pool(host='localhost', port=3306, user='root', password='12345678', db='sovk', minsize=1, maxsize=100)
    await bot.delete_webhook(drop_pending_updates=True)
    scheduler = AsyncIOScheduler()
    scheduler.add_job(algorithm, args=[bot], trigger=IntervalTrigger(seconds=2))
    scheduler.start()
    await dp.start_polling(bot)


async def start_message():
    await bot.send_message(chat_id=Admin.id_chat_users, text="Бот заработал")


async def end_message():
    await bot.send_message(chat_id=Admin.id_chat_users, text="@qwark666 Бот упал. Поднимите его")


if __name__ == "__main__":
    asyncio.run(main())
