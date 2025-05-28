import asyncio
import os
import re
from collections import defaultdict

from aiogram import Bot, types
from dotenv import load_dotenv, find_dotenv
from telethon import events
from telethon.sync import TelegramClient

from database import insert_data, select_users2, get_user
from info import Admin, keyboard1
load_dotenv(find_dotenv())
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone = os.getenv('NUMBER')
client = TelegramClient('session_name', int(api_id), api_hash)


global data_now_user
global flag # 1 inn_dir2  2 inn_own2 3 inn_dir1 4 inn_own1
global semaphore
global bot

async def send_message(text:str):
    if text == '-':
        return
    await client.send_message(bot.id, text)



async def auth():
    global semaphore
    semaphore = asyncio.Semaphore(1)  # опять ебаные семафоры, я надеялся забыть это
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
    bot = await client.get_entity(os.getenv('BOT')) # сюда добавить проверку существует ли тг акк глаза бога



@client.on(events.MessageEdited())
async def handler(event):
    if 'Отчет слишком большой' in event.message.message:
        return
    await asyncio.sleep(4)
    await extract_name_and_phone(event.message.message)





async def extract_name_and_phone(text:str) -> None:
    name_pattern = r"ФИО: ([А-ЯЁ][а-яё]+\s[А-ЯЁ][а-яё]+\s[А-ЯЁ][а-яё]+)\n"
    name_match = re.search(name_pattern, text)
    name = name_match.group(1) if name_match else ''
    if not name:
        print(1)
        name_pattern = r'''Лица:\n└ ([А-ЯЁ][а-яё]+\s[А-ЯЁ][а-яё]+\s[А-ЯЁ][а-яё]+)\n'''
        name_match = re.search(name_pattern, text)
        name = name_match.group(1) if name_match else ''

    if not name:
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
    phone_match = ', '.join(phone_match)
    global flag
    if not name:
        name = '-'
    if not phone_match:
        phone_match = '-'
    if name != '-' or phone_match != '-':
        if flag == 1:
            if data_now_user['ИНН_DIR2_name'] == '-' and data_now_user['ИНН_DIR2_phone'] == '-':
                data_now_user['ИНН_DIR2_name'] = [name, ]
                data_now_user['ИНН_DIR2_phone'] = [phone_match, ]
            else:
                data_now_user['ИНН_DIR2_name'].append(name)
                data_now_user['ИНН_DIR2_phone'].append(phone_match)
        elif flag == 2:
            if data_now_user['ИНН_OWN2_name'] == '-' and data_now_user['ИНН_OWN2_phone'] == '-':
                data_now_user['ИНН_OWN2_name'] = [name, ]
                data_now_user['ИНН_OWN2_phone'] = [phone_match, ]
            else:
                data_now_user['ИНН_OWN2_name'].append(name)
                data_now_user['ИНН_OWN2_phone'].append(phone_match)
        elif flag == 3:
            if data_now_user['ИНН_DIR1_name'] == '-' and data_now_user['ИНН_DIR1_phone'] == '-':
                data_now_user['ИНН_DIR1_name'] = [name, ]
                data_now_user['ИНН_DIR1_phone'] = [phone_match, ]
            else:
                data_now_user['ИНН_DIR1_name'].append(name)
                data_now_user['ИНН_DIR1_phone'].append(phone_match)
        elif flag == 4:
            if data_now_user['ИНН_OWN1_name'] == '-' and data_now_user['ИНН_OWN1_phone'] == '-':
                data_now_user['ИНН_OWN1_name'] = [name, ]
                data_now_user['ИНН_OWN1_phone'] = [phone_match, ]
            else:
                data_now_user['ИНН_OWN1_name'].append(name)
                data_now_user['ИНН_OWN1_phone'].append(phone_match)

        elif flag == 99:
            data_now_user['solo'] = [f'{name} {phone_match}']
        else:
            pass
    global semaphore
    semaphore.release()
    return


async def get_users_data(a:defaultdict, sm: asyncio.Semaphore, i: str, bt: Bot, flg :int = 1, chat: int=Admin.id_chat_users):
    global data_now_user
    global flag
    data_now_user = a
    global semaphore
    if not semaphore:
        semaphore = asyncio.Semaphore(1) #опять ебаные семафоры, я надеялся забыть это

    # await semaphore.acquire()
    # flag = 1
    # if len(str(data_now_user['ИНН_DIR2'])) == 12:
    #     await send_message(str(data_now_user['ИНН_DIR2']))
    # else:
    #     semaphore.release()
    #
    #
    # for j in data_now_user['ИНН_OWN2']:
    #     await semaphore.acquire()
    #     flag = 2
    #     if len(str(j)) == 12:
    #         await send_message(str(j))
    #     else:
    #         semaphore.release()

    for j in data_now_user['ИНН_DIR1']:
        await semaphore.acquire()
        flag = 3
        if len(str(j)) == 12:
            await send_message(str(j))
        else:
            semaphore.release()

    for j in data_now_user['ИНН_OWN1']:
        await semaphore.acquire()
        flag = 4
        if len(str(j)) == 12:
            await send_message(str(j))
        else:
            semaphore.release()
    a = list(data_now_user['ИНН_OWN1'])
    data_now_user['ИНН_OWN1'] = []
    for f in a: # ВСЮ ЭТУ ДИЧЬ ДЕЛИТНУТЬ НАХУЙ КОГДА ДОБАВЛЮ РЕКРСИВНЫЙ ОБХОД КОМПАНИЙ У КОТОРЫХ УЧРЕДЫ - ООО
        if len(str(f)) == 12:
            data_now_user['ИНН_OWN1'].append(f)

    a = list(data_now_user['ИНН_DIR1'])
    data_now_user['ИНН_DIR1'] = []
    for f in a:
        if len(str(f)) == 12:
            data_now_user['ИНН_DIR1'].append(f)


    await semaphore.acquire()
    semaphore.release()
    await insert_data(data_now_user, i)
    if flg == 1:
        stri = f'''<b>❗Найден новый lead №{data_now_user['counter']}❗</b>
<b>C сайта ЕАС/контракты</b>
<a href="{data_now_user['link']}">Ссылка на контракт </a>
<b>Объект закупки: {data_now_user['name']}</b>
<b>Стоимость контракта {data_now_user['cost']}</b>
<b>Дата контракта {data_now_user['date']}</b>
<b>-------------------------------</b>
<b>Исполнитель</b>
<b>Название: {data_now_user['NAME1']}</b>
<b>ИНН <code>{i}</code></b>
<b>Контакты с сайта {data_now_user['cont_from_page']}</b>
<b>Директора:</b>'''
        for i in range(len(data_now_user['ИНН_DIR1'])):
            stri += f'''<b>\nИНН <code>{data_now_user['ИНН_DIR1'][i]}</code></b>
<b>Имя {'Найдено' if data_now_user['ИНН_DIR1_name'][i] != '-' else 'Не найдено'}</b>
<b>Телефон {'Найден' if data_now_user['ИНН_DIR1_phone'][i] != '-' else 'Не найден'}</b>'''
        stri +='''\n<b>Учредители:</b>'''
        for i in range(len(data_now_user['ИНН_OWN1'])):
            stri += f'''<b>\nИНН <code>{data_now_user['ИНН_OWN1'][i]}</code></b>
<b>Имя {'Найдено' if data_now_user['ИНН_OWN1_name'][i] != '-' else 'Не найдено'}</b>
<b>Телефон {'Найден' if data_now_user['ИНН_OWN1_phone'][i] != '-' else 'Не найден'}</b>'''

        stri += '\n<b>-------------------------------</b>'
    else:
        stri = f'''
<b>Название: {data_now_user['NAME1']}</b>
<b>ИНН <code>{i}</code></b>
<b>ИНН директора <code>{data_now_user['ИНН_DIR1']}</code></b>
<b>ИНН учредителей <code>{', '.join(data_now_user['ИНН_OWN1'])}</code></b>
<b>Контакты директора {data_now_user['ИНН_DIR1_contacts']}</b>
<b>Контакты учредителей {', '.join(data_now_user['ИНН_OWN1_contacts'])}</b>
<b>-------------------------------</b>'''
    await bt.send_message(Admin.id_chat_test, stri, parse_mode="HTML", reply_markup=keyboard1)
    sm.release()


async def get_one_user(i:str, bt: Bot, chat: int):
    global semaphore
    if not semaphore:
        semaphore = asyncio.Semaphore(1)  # опять ебаные семафоры, я надеялся забыть это
    global data_now_user
    global flag
    flag = 99
    data_now_user = defaultdict(lambda : '-')
    await semaphore.acquire()
    await send_message(i)
    await semaphore.acquire()
    semaphore.release()
    await bt.send_message(chat, ' '.join(data_now_user['solo']), parse_mode="HTML")

async def edit_message(callback_query: types.CallbackQuery, bt: Bot):
    a = callback_query.message.text
    num = 0
    for i in range(a.find('№') + 1, 100):
        if a[i] != '❗':
            num  = num * 10 + int(a[i])
        else:
            break
    global data_now_user
    data_now_user = defaultdict(lambda : '-')
    await select_users2(num, data_now_user) # добавить выдачу данных из бд
    await get_user(num, callback_query)
    print(data_now_user)
    stri = f'''<b>❗Найден новый lead №{data_now_user['counter']}❗</b>
<b>C сайта ЕАС/контракты</b>
<a href="{data_now_user['link']}">Ссылка на контракт </a>
<b>Объект закупки: {data_now_user['name']}</b>
<b>Стоимость контракта {data_now_user['cost']}</b>
<b>Дата контракта {data_now_user['date']}</b>
<b>-------------------------------</b>
<b>Исполнитель</b>
<b>Название: {data_now_user['NAME1']}</b>
<b>ИНН <code>{data_now_user['ИНН_slave1']}</code></b>
<b>Контакты с сайта {data_now_user['cont_from_page']}</b>
<b>Директор:</b>'''
    for i in range(len(data_now_user['ИНН_DIR1'])):
        stri += f'''<b>\nИНН <code>{data_now_user['ИНН_DIR1'][i]}</code></b>
<b>Имя {data_now_user['ИНН_DIR1_name'][i]}</b>
<b>Телефон {data_now_user['ИНН_DIR1_phone'][i]}</b>'''
    stri += '''\n<b>Учредители:</b>'''
    for i in range(len(data_now_user['ИНН_OWN1'])):
        stri += f'''<b>\nИНН <code>{data_now_user['ИНН_OWN1'][i]}</code></b>
<b>Имя {data_now_user['ИНН_OWN1_name'][i]}</b>
<b>Телефон {data_now_user['ИНН_OWN1_phone'][i]}</b>'''

    stri += '\n<b>-------------------------------</b>'
    chat = await bt.get_chat(callback_query.from_user.id)
    try:
        stri += f'\nЛида забрал @{chat.username}'
    except:
        stri += '\nЛида забрал @человек_без_юзернейма'
    await callback_query.message.edit_text(stri, parse_mode="HTML")
