from aiogram import Router, types, Bot, F
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext

from database import export_mysql_to_excel
from info import users, User
from main import process_user
from tg import get_one_user

admins_router = Router()
global bot
async def create_admins_router(bt: Bot):
    global bot
    bot = bt


@admins_router.message(StateFilter(None), Command("data"))
async def execl(message: types.Message, state: FSMContext):
    if await export_mysql_to_excel():
        await bot.send_document(message.chat.id, types.FSInputFile(path="data.xlsx"))
    else:
        await bot.send_message(message.chat.id, 'Файл утерялся @qwark666')

@admins_router.message(StateFilter(None), Command("find"))
async def start(message: types.Message, state: FSMContext):
    if message.from_user.id not in users:
        return
    await bot.send_message(message.chat.id, "Отправьте ИНН")
    await state.set_state(User.find)


@admins_router.message(User.find, F.text)
async def find(message: types.Message, state: FSMContext):
    if message.from_user.id not in users:
        return
    try:
        int(message.text)
    except ValueError:
        await message.answer('Неправильный формат')
        await state.clear()
    if len(message.text) == 10:
        await process_user(message.text, 2, message.from_user.id)
        await state.clear()
    elif len(message.text) == 12:
        await get_one_user(message.text, bot, message.from_user.id)
        await state.clear()
    else:
        await message.answer('Неправильный формат')
        await state.clear()