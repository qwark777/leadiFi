import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv, find_dotenv

from database import create_con_pol, add_user, alarm
from info import Admin, keyboard2, keyboard1
from main import algorithm, sub_dp
from tg import auth

load_dotenv(find_dotenv())
bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()
dp.include_router(sub_dp)



@dp.callback_query(StateFilter(None), lambda c: c.data and c.data.startswith('btn_1_'))
async def get_tel(callback_query: types.CallbackQuery, state: FSMContext):
    index = int(callback_query.data.split("_")[-1])
    await bot.answer_callback_query(callback_query.id)
    if index == 1:
        await callback_query.message.edit_text(text=callback_query.message.text, reply_markup=keyboard2)
    elif index == 2:
        chat = await bot.get_chat(callback_query.from_user.id)
        try:
            await callback_query.message.edit_text(text=callback_query.message.text + '\nЛида забрал @' + chat.username, reply_markup=None)
        except:
            await callback_query.message.edit_text(text=callback_query.message.text + '\nЛида забрал @' + 'человек без username', reply_markup=None)
        await add_user(callback_query.from_user.id, callback_query.message.message_id)
    elif index == 3:
        await callback_query.message.edit_text(text=callback_query.message.text, reply_markup=keyboard1)


async def main():
    # dp.startup.register(start_message)
    # dp.shutdown.register(end_message)
    await bot.delete_webhook(drop_pending_updates=True)
    scheduler = AsyncIOScheduler()
    await auth()
    await create_con_pol()
    scheduler.add_job(algorithm, args=[bot], trigger=CronTrigger(hour=13, minute=58, timezone='Europe/Moscow'))
    scheduler.add_job(alarm, args=[bot], trigger=CronTrigger(hour=10, minute=0, timezone='Europe/Moscow'))
    scheduler.start()
    await dp.start_polling(bot)


async def start_message():
    await bot.send_message(chat_id=Admin.id_chat_users, text="Бот заработал")


async def end_message():
    await bot.send_message(chat_id=Admin.id_chat_users, text="@qwark666 Бот упал. Поднимите его")


if __name__ == "__main__":
    asyncio.run(main())
