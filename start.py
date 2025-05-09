import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv, find_dotenv
from admins_router import admins_router, create_admins_router
from database import create_con_pol, alarm, export_mysql_to_excel
from info import Admin, keyboard2, keyboard1, find_keyboard, User
from main import algorithm, sub_dp, process_user, create_main
from tg import auth, get_users_data, get_one_user, edit_message

load_dotenv(find_dotenv())
bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()
dp.include_router(sub_dp)
dp.include_router(admins_router)


@dp.callback_query(StateFilter(None), lambda c: c.data and c.data.startswith('btn_1_'))
async def get_tel(callback_query: types.CallbackQuery, state: FSMContext):
    index = int(callback_query.data.split("_")[-1])
    await bot.answer_callback_query(callback_query.id)
    if index == 1:
        await callback_query.message.edit_text(text=callback_query.message.html_text, reply_markup=keyboard2,  parse_mode="HTML")
    elif index == 2:
        await edit_message(callback_query)
    elif index == 3:
        await callback_query.message.edit_text(text=callback_query.message.html_text, reply_markup=keyboard1,  parse_mode="HTML")


async def main():
    # dp.startup.register(start_message)
    # dp.shutdown.register(end_message)
    await bot.delete_webhook(drop_pending_updates=True)
    scheduler = AsyncIOScheduler()
    await auth()
    await create_con_pol()
    await create_admins_router(bot)
    await create_main(bot)
    scheduler.add_job(algorithm, trigger=CronTrigger(hour=10, minute=47, timezone='Europe/Moscow'))
    scheduler.add_job(alarm, args=[bot], trigger=CronTrigger(hour=10, minute=0, timezone='Europe/Moscow'))
    scheduler.start()
    await dp.start_polling(bot)


async def start_message():
    await bot.send_message(chat_id=Admin.id_chat_users, text="Бот заработал")


async def end_message():
    await bot.send_message(chat_id=Admin.id_chat_users, text="@qwark666 Бот упал. Поднимите его")


if __name__ == "__main__":
    asyncio.run(main())
