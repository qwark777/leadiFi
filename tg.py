import asyncio
import os
import re
from collections import defaultdict
from dotenv import load_dotenv, find_dotenv
from telethon import events
from telethon.sync import TelegramClient


load_dotenv(find_dotenv())
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone = os.getenv('NUMBER')
client = TelegramClient('session_name', int(api_id), api_hash)


global inn
global flag # 1 inn_dir2  2 inn_own2 3 inn_dir1 4 inn_own1
global inn_one

async def send_message(text:str):
    bot = await client.get_entity(os.getenv('BOT'))
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



@client.on(events.NewMessage())
async def handler(event):
    try:
        if "подождите" in event.message.message:
            return
        await extract_name_and_phone(event.message.message) # это короче текст смс
    except Exception as e:
        print(f"❌ Ошибка: {e}")



async def extract_name_and_phone(text:str) -> None:
    name_pattern = r"([А-ЯЁ][а-яё]+\s[А-ЯЁ][а-яё]+\s[А-ЯЁ][а-яё]+)"
    name_match = re.search(name_pattern, text)
    name = name_match.group(1) if name_match else None

    phone_pattern = r"(\+\d{11})"
    phone_match = re.findall(phone_pattern, text)

    if flag == 1:
        inn[inn_one]['ИНН_DIR2_contacts'] = name, phone_match
    elif flag == 2:
        if inn[inn_one]['ИНН_OWN2_contacts'] == '-':
            inn[inn_one]['ИНН_OWN2_contacts'] = [(name, phone_match), ]
        else:
            inn[inn_one]['ИНН_OWN2_contacts'].append((name, phone_match))
    elif flag == 3:
        inn[inn_one]['ИНН_DIR1_contacts'] = name, phone_match
    elif flag == 4:
        if inn[inn_one]['ИНН_OWN1_contacts'] == '-':
            inn[inn_one]['ИНН_OWN1_contacts'] = [(name, phone_match), ]
        else:
            inn[inn_one]['ИНН_DIR1_contacts'].append((name, phone_match))
    else:
        pass
    return

async def get_users_data(a:defaultdict):
    global inn
    global flag
    global inn_one

    inn = a
    semaphore = asyncio.Semaphore(1) #опять ебаные семафоры, я надеялся забыть это
    for i in inn.keys():
        inn_one = i

        await semaphore.acquire()
        flag = 1
        await send_message(str(inn[i]['ИНН_DIR2']))

        for j in inn[i]['ИНН_OWN2']:
            await semaphore.acquire()
            flag = 2
            await send_message(str(j))

        await semaphore.acquire()
        flag = 3
        await send_message(str(inn[i]['ИНН_DIR1']))

        for j in inn[i]['ИНН_OWN1']:
            await semaphore.acquire()
            flag = 4
            await send_message(str(j))





text = """
# Отчет по ИНН:

## Возможные связи:

- Олейников Игорь Васильевич  
  1977–10–13  (47 лет)

---

### Контакты:

- +79028154872
- +79345135872  
- Тюменская область  
- Google | Яндекс | WhatsApp  

- oleinikov.1310@yandex.ru  
- Google | Яндекс  

---

Сайт 💬 Ревервный Бот 4 📧 VPN
"""



