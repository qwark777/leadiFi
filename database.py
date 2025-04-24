import aiomysql
from aiogram import Bot
from openpyxl import Workbook

from info import Admin

global pool


async def create_con_pol():
    global pool
    pool = await aiomysql.create_pool(host='localhost', port=3306, user='root', password='12345678', db='sovk',
                                      minsize=1, maxsize=100, pool_recycle=3600)


async def add_user(id_user: int, id_message: int) -> bool:
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
    string = f'SELECT * FROM users WHERE CURDATE() >= DATE_ADD(data, INTERVAL 7 day)'
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(string)
                result_set = await cursor.fetchall()
                for i in result_set:
                    if i[0] == 0:
                        return
                    chat = await bot.get_chat(i[0])
                    await bot.send_message(Admin.id_chat_users, f'Напоминаю @{chat.username} о клиенте',
                                           reply_to_message_id=i[2])
                    st = f'DELETE FROM users WHERE id_message={i[2]}'
                    async with pool.acquire() as con:
                        async with con.cursor() as cur:
                            await cur.execute(st)
                            await cur.fetchall()
                        await con.commit()
                await conn.commit()
        return False
    except Exception as e:
        print(e)
        return True


async def export_mysql_to_excel():
    try:
        async with pool.acquire() as conn:
            wb = Workbook()
            wb.remove(wb.active)

            async with conn.cursor() as cursor:
                await cursor.execute("SELECT * FROM users")
                data = await cursor.fetchall()
                ws = wb.create_sheet(title='data')  # Ограничение на 31 символ
                if not data:
                    return False
                headers = [desc[0] for desc in cursor.description]
                ws.append(headers)
                for row in data:
                    ws.append(row)
                await conn.commit()
            filename = "data.xlsx"
            wb.save(filename)

    except Exception as e:
        print(f"Ошибка при экспорте: {e}")
        return False
    return True


async def insert_data(inn: dict, i: str):
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                string = f"""INSERT INTO users (id_user, data, id_message, link, name, cost, date, name1, inn1, inn_dir1, inn_own1, contact_site, contact_dir1, contact_own1 ) VALUES ( 0, CURDATE(), 0, '{inn['link']}', '{inn['name']}', '{inn['cost']}', '{inn['date']}', '{inn['NAME1']}', '{i}', '{inn['ИНН_DIR1']}', '{', '.join(inn['ИНН_OWN1'])}', '{inn['cont_from_page']}', '{inn['ИНН_DIR1_contacts'][0]}', '{inn['ИНН_DIR1_contacts'][0]}')"""
                await cursor.execute(string)
                await cursor.fetchall()
                await conn.commit()

    except Exception as e:
        print(f"Ошибка при экспорте: {e}")
        return False
    return True
