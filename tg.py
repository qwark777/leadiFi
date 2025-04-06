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
    await client.run_until_disconnected()
    print("✅ Успешный вход! ID:", (await client.get_me()).id)



@client.on(events.NewMessage())
async def handler(event):
    try:
        print(event.message.message) #это короче текст смс
    except Exception as e:
        print(f"❌ Ошибка: {e}")



async def extract_name_and_phone(text:str) -> bool:
    name_pattern = r"([А-ЯЁ][а-яё]+\s[А-ЯЁ][а-яё]+\s[А-ЯЁ][а-яё]+)\s*\n\s*\d{4}–\d{2}–\d{2}"
    name_match = re.search(name_pattern, text)
    name = name_match.group(1) if name_match else None

    phone_pattern = r"(\+\d{11})"
    phone_match = re.search(phone_pattern, text)
    phone = phone_match.group(1) if phone_match else None

    #здесь должна быть вставка в ебаный словарь

    return name or phone


async def get_users_data(a:defaultdict):
    global inn
    inn = a
    semaphore = asyncio.Semaphore(1) #опять ебаные семафоры, я надеялся забыть это
    for i in inn.keys():
        await semaphore.acquire()
        await send_message(str(i))





asyncio.run(auth())




