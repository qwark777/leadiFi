import asyncio
from collections import defaultdict

from aiogram import Bot
from aiogram import Router, types

from database import users_transfer, select_users1, check_user
from eac import eac
from info import Admin, keyboard3
from nal import process_inn
from pdf import pdf_parcer1
from tg import get_users_data

global inn
global bot

sub_dp = Router()
sem = asyncio.Semaphore(1)

async def create_main(bt: Bot):
    global bot
    bot = bt
    global inn
    inn = defaultdict(lambda : defaultdict(lambda :'-'))
@sub_dp.callback_query(lambda c: c.data and c.data.startswith('btn_2_'))
async def continue_registration_calling(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    index = int(callback_query.data.split("_")[-1])
    global inn
    if not inn:
        inn = defaultdict(lambda : defaultdict(lambda : '-'))
    if index == 1:
        await callback_query.message.edit_text('Обработка 🔄', reply_markup=None)
        await select_users1(callback_query.message.text.split('\n')[0], inn[callback_query.message.text.split('\n')[1]])
        await process_user(callback_query.message.text.split('\n')[1])
        await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    elif index == 2:
        await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)

async def algorithm():
    global inn
    inn = await eac()
    keys = list(inn.keys())
    for i in keys:
        if await check_user(inn[i]['name']):
            del inn[i]
    flag = await users_transfer(inn)
    await bot.send_message(Admin.id_chat_ivan, "Бот отработал корректно смс отправлено")
    await check_names()

async def check_names():
    global inn
    for i in inn.keys():
        await bot.send_message(Admin.id_chat_ivan, f'{inn[i]['counter']}\n{i}\n{inn[i]['name']}\n{inn[i]['cost']}', reply_markup=keyboard3)
    inn = defaultdict(lambda: defaultdict(lambda: '-'))


async def process_user(i:str, flg: int = 1, chat: int=Admin.id_chat_users):
    if i != '-':
        if not await process_inn(i):
            await asyncio.sleep(60)
            await process_inn(i)
        await pdf_parcer1(fr"sovk/{i}.pdf", inn[i])
    # if inn[i]['inn_owner'] != '-':
    #     if not await process_inn(inn[i]['inn_owner']):
    #         await asyncio.sleep(60)
    #         await process_inn(inn[i]['inn_owner'])
    #     await pdf_parcer2(fr"sovk/{inn[i]['inn_owner']}.pdf", inn[i])
    else:
        print(f'Lost file{i}')
    await sem.acquire()
    await get_users_data(inn[i], sem, i, bot, flg)



