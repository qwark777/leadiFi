import aiomysql
from aiogram import Bot

from info import Admin

global pool
async def create_con_pol():
    global pool
    pool = await aiomysql.create_pool(host='localhost', port=3306, user='root', password='12345678', db='sovk', minsize=1, maxsize=100, pool_recycle=3600)


async def add_user(id_user: int, id_message:int) -> bool:
    string = f'INSERT users(id_user, data, id_message) VALUES ({id_user}, CURDATE(), {id_message})'
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(string)
                await cursor.fetchall()
                await conn.commit()
        return False
    except Exception as e:
        print(e)
        return True

async def alarm(bot: Bot):
    string  = f'SELECT * FROM users WHERE CURDATE() >= DATE_ADD(data, INTERVAL 0 day)'
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(string)
                result_set = await cursor.fetchall()
                for i in result_set:
                    chat = await bot.get_chat(i[0])
                    await bot.send_message(Admin.id_chat_users, f'Напоминаю @{chat.username} о клиенте', reply_to_message_id=i[2])
                await conn.commit()
        return False
    except Exception as e:
        print(e)
        return True