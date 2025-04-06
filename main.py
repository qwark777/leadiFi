import asyncio
from collections import defaultdict

from aiogram import Bot

from eac import eac
from god_eye import probiv
from info import Admin, pattern, pattern_for_group, keyboard1
from nal import process_inn
from pdf import pdf_parcer1, pdf_parcer2

global inn

async def algorithm(bot: Bot):
    global inn
    inn = await eac()
    for i in inn.keys():
        if not await process_inn(i):
            await subprocess(bot)
            await asyncio.sleep(60)
            await process_inn(i)
        if not await process_inn(inn[i]['inn_owner']):
            await subprocess(bot)
            await asyncio.sleep(60)
            await process_inn(inn[i]['inn_owner'])
    await subprocess(bot)


async def subprocess(bot:Bot):
    for i in inn.keys():
        if await pdf_parcer1(fr"C:\sovk\{i}.pdf", inn[i]) and await pdf_parcer2(fr"C:\sovk\{inn[i]['inn_owner']}.pdf",
                                                                                inn[i]):
            # await probiv(i, inn)
            pass
        else:
            print(f'Lost file{i}')
    for i in inn.keys():
        await print_form(i, bot)



counter = 0


async def print_form_form(i: str, bot: Bot, arr: list):
    global counter
    stri = pattern_for_group
    await bot.send_message(Admin.id_chat_users,
                           stri.format(i=counter, link=inn[i]['link'], name=inn[i]['name'], cost=inn[i]['cost'],
                                       date=inn[i]['date'], inn_owner=inn[i]['inn_owner'],
                                       i_dir2=inn[i]['ИНН_DIR2'], i_own2=', '.join(inn[i]['ИНН_OWN2']), i_con_dir2=arr[1], i_con_own2= arr[2],
                                       inn_slave=i, i_dir1=inn[i]['ИНН_DIR1'], i_own1=', '.join(inn[i]['ИНН_OWN1']),
                                       cont_from_page=inn[i]['cont_from_page'], i_con_dir1=arr[3], i_con_own1= arr[4]), parse_mode="HTML", reply_markup=keyboard1)


async def print_form(i: int, bot: Bot):
    stri = pattern
    global counter
    counter += 1
    await bot.send_message(Admin.id_ivan_id,
                           stri.format(i=counter, link=inn[i]['link'], name=inn[i]['name'], cost=inn[i]['cost'],
                                       date=inn[i]['date'], inn_owner=inn[i]['inn_owner'],
                                       i_dir2=inn[i]['ИНН_DIR2'], i_own2=', '.join(inn[i]['ИНН_OWN2']),
                                       inn_slave=i, i_dir1=inn[i]['ИНН_DIR1'], i_own1=', '.join(inn[i]['ИНН_OWN1']),
                                       cont_from_page=inn[i]['cont_from_page']), parse_mode="HTML")


global now_inn


