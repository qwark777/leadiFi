import asyncio
import os

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



@dp.message(StateFilter(None), F.text)
async def get_tel(message: types.Message, state: FSMContext):
    a = message.text.split('\n')
    await print_form_form(str(a[0]), bot, a)





async def main():
    # dp.startup.register(start_message)
    # dp.shutdown.register(end_message)
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
