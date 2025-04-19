import asyncio
import os
import re
import time
from collections import defaultdict

from aiogram import Bot
from dotenv import load_dotenv, find_dotenv
from telethon import events
from telethon.sync import TelegramClient

from info import pattern_for_group, Admin, keyboard1

load_dotenv(find_dotenv())
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone = os.getenv('NUMBER')
client = TelegramClient('session_name', int(api_id), api_hash)


global inn
global flag # 1 inn_dir2  2 inn_own2 3 inn_dir1 4 inn_own1
global semaphore
global bot
sem = None

async def send_message(text:str):
    if text == '-':
        return
    await client.send_message(bot.id, text)



async def auth():
    await client.connect()
    if not await client.is_user_authorized():
        try:
            await client.send_code_request(phone)
            code = input("✉️ Введите код из SMS: ")
            await client.sign_in(phone, code)
        except Exception as e:
            print(e)
    print("✅ Успешный вход! ID:", (await client.get_me()).id)
    global bot
    bot = await client.get_entity(os.getenv('BOT')) # сюда добавить проверку



@client.on(events.MessageEdited())
async def handler(event):
    await asyncio.sleep(4)
    await extract_name_and_phone(event.message.message, semaphore)





async def extract_name_and_phone(text:str, sm:asyncio.Semaphore) -> None:
    name_pattern = r"ФИО: ([А-ЯЁ][а-яё]+\s[А-ЯЁ][а-яё]+\s[А-ЯЁ][а-яё]+)\n"
    name_match = re.search(name_pattern, text)
    name = name_match.group(1) if name_match else ''
    if name is None:
        name_pattern = r"Имя: ([А-ЯЁ][а-яё]+)\n"
        name_match = re.search(name_pattern, text)
        firstname = name_match.group(1) if name_match else ''
        name_pattern = r"Фамилия: ([А-ЯЁ][а-яё]+)\n"
        name_match = re.search(name_pattern, text)
        surname = name_match.group(1) if name_match else ''
        name_pattern = r"Отчество: ([А-ЯЁ][а-яё]+)\n"
        name_match = re.search(name_pattern, text)
        father = name_match.group(1) if name_match else ''
        name = surname + firstname + father

    phone_pattern = r"(\+\d{11})"
    phone_match = re.findall(phone_pattern, text)
    global flag
    if not name:
        name = '-'
    if not phone_match:
        phone_match = '-'
    if name or phone_match:
        if flag == 1:
            inn['ИНН_DIR2_contacts'] = name, phone_match
        elif flag == 2:
            if inn['ИНН_OWN2_contacts'] == '-':
                inn['ИНН_OWN2_contacts'] = [f'{name} {phone_match}', ]
            else:
                inn['ИНН_OWN2_contacts'].append(f'{name}{phone_match}')
        elif flag == 3:
            inn['ИНН_DIR1_contacts'] = name, phone_match
        elif flag == 4:
            if inn['ИНН_OWN1_contacts'] == '-':
                inn['ИНН_OWN1_contacts'] = [f'{name} {phone_match}', ]
            else:
                inn['ИНН_OWN1_contacts'].append(f'{name} {phone_match}')
        else:
            pass
    sm.release()
    return

counter = 0

async def get_users_data(a:defaultdict, sm: asyncio.Semaphore, i: str, bt: Bot):
    global sem
    sem = sm
    global inn
    global flag
    inn = a
    global semaphore
    semaphore = asyncio.Semaphore(1) #опять ебаные семафоры, я надеялся забыть это


    await semaphore.acquire()
    flag = 1
    if len(str(inn['ИНН_DIR2'])) == 12:
        await send_message(str(inn['ИНН_DIR2']))
    else:
        semaphore.release()


    for j in inn['ИНН_OWN2']:
        await semaphore.acquire()
        flag = 2
        if len(str(j)) == 12:
            await send_message(str(j))
        else:
            semaphore.release()

    await semaphore.acquire()
    flag = 3
    if len(str(inn['ИНН_DIR1'])) == 12:
        await send_message(str(inn['ИНН_DIR1']))
    else:
        semaphore.release()

    for j in inn['ИНН_OWN1']:
        await semaphore.acquire()
        flag = 4
        if len(str(j)) == 12:
            await send_message(str(j))
        else:
            semaphore.release()

    await semaphore.acquire()
    semaphore.release()
    global counter
    stri = pattern_for_group

    await bt.send_message(Admin.id_chat_users,
                           stri.format(i=counter, link=inn['link'], name=inn['name'], cost=inn['cost'],
                                       date=inn['date'], inn_owner=inn['inn_owner'],
                                       i_dir2=inn['ИНН_DIR2'], i_own2=', '.join(inn['ИНН_OWN2']),
                                       i_con_dir2=inn['ИНН_DIR2_contacts'][0] +  str(inn['ИНН_DIR2_contacts'][1]),
                                       i_con_own2= '| '.join(list(inn['ИНН_OWN2_contacts'])),
                                       inn_slave=i, i_dir1=inn['ИНН_DIR1'], i_own1=', '.join(inn['ИНН_OWN1']),
                                       cont_from_page=inn['cont_from_page'],
                                       i_con_dir1=inn['ИНН_DIR1_contacts'][0]  + str(inn['ИНН_DIR1_contacts'][1]),
                                       i_con_own1= ' | '.join(list(inn['ИНН_OWN1_contacts']))), parse_mode="HTML",
                           reply_markup=keyboard1)
    sem.release()


