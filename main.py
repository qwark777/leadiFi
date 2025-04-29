import asyncio
from collections import defaultdict

from aiogram import Bot
from aiogram import Router, types
from numpy.random import default_rng

from eac import eac
from info import Admin, keyboard3
from nal import process_inn
from pdf import pdf_parcer1, pdf_parcer2
from tg import send_message, get_users_data

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
    if index == 1:
        await process_user(callback_query.message.text.split('\n')[0])
        await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    elif index == 2:
        del inn[callback_query.message.text.split('\n')[0]]
        await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)

async def algorithm(bt: Bot):
    global inn
    inn = await eac()
    await  check_names()

async def check_names():
    for i in inn.keys():
        await bot.send_message(Admin.id_ivan_id, "Бот отработал корректно смс отправлено")
        await bot.send_message(Admin.id_alex_chat, f'{i}\n{inn[i]['name']}\n{inn[i]['cost']}', reply_markup=keyboard3)

async def process_user(i:str, flg: int = 1):
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



