from collections import defaultdict
import aiomysql
from aiogram import Bot, types
from openpyxl import Workbook
from info import Admin


global pool


async def create_con_pol():
    global pool
    pool = await aiomysql.create_pool(host='localhost', port=3306, user='root', password='12345678', db='sovk',
                                      minsize=1, maxsize=100, pool_recycle=3600)


async def alarm(bot: Bot):
    string = f'SELECT id_user, data, id_message FROM users WHERE CURDATE() >= DATE_ADD(data, INTERVAL 7 day)'
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(string)
                result_set = await cursor.fetchall()
                for i in result_set:
                    if i[0] == 0 or i[2] == 0:
                        return
                    chat = await bot.get_chat(i[0])
                    await bot.send_message(Admin.test_chat, f'Напоминаю @{chat.username} о клиенте',
                                           reply_to_message_id=i[2])
                    st = f"""UPDATE users set data = CURDATE() where id_message={i[2]}"""
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
        print(f"Ошибка при экспорте: {e}", export_mysql_to_excel.__name__)
        return False
    return True


async def insert_data(inn: dict, i: str):
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                string = f"""INSERT INTO users set id_user = 0, id_message = 0, link = '{inn['link']}', name = '{inn['name']}', cost = '{inn['cost']}', date = '{inn['date']}' , name1 = '{inn['NAME1']}', inn1 = '{i}', inn_dir1 = '{', '.join(inn['ИНН_DIR1'])}', inn_own1 = '{', '.join(inn['ИНН_OWN1'])}', contact_site = '{inn['cont_from_page']}', name_dir1 = '{'|'.join(inn['ИНН_DIR1_name'])}', phone_dir1 = '{'|'.join(inn['ИНН_DIR1_phone'])}', name_own1 = '{'|'.join(inn['ИНН_OWN1_name'])}', phone_own1 = '{'|'.join(inn['ИНН_OWN1_phone'])}', id_eac = '{inn['counter']}'"""
                await cursor.execute(string)
                await cursor.fetchall()
                await conn.commit()

    except Exception as e:
        print(f"Ошибка при экспорте: {e}", insert_data.__name__)
        return False
    return True


async def users_transfer(inn:defaultdict):
    for i in inn:
        try:
            async with pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    string = f"""INSERT INTO eac (link, name, cost, date, inn1, contact_site) VALUES ('{inn[i]['link']}', '{inn[i]['name']}', '{inn[i]['cost']}', '{inn[i]['date']}', '{i}', '{inn[i]['cont_from_page']}')"""
                    await cursor.execute(string)
                    await cursor.fetchall()
                    last_id = cursor.lastrowid
                    inn[i]['counter'] = last_id
                    await conn.commit()
        except Exception as e:
            print(f"Ошибка при экспорте: {e}", users_transfer.__name__)
            return False
    return True

async def select_users1(id_: str, inn: defaultdict):
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                string = f"""select link, name, cost, date, inn1, contact_site from eac where id = {id_}"""
                await cursor.execute(string)
                ans = (await cursor.fetchall())[0]
                inn['link'], inn['name'],  inn['cost'], inn['date'], inn['ИНН_slave1'], inn['cont_from_page'], inn['counter'] = ans[0], ans[1], ans[2], ans[3], ans[4], ans[5], id_
                await conn.commit()
    except Exception as e:
        print(f"Ошибка при экспорте: {e}", select_users1.__name__)
        return False
    return True

async def select_users2(id_: str, inn: defaultdict):
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                string = f"""select link, name, cost, date, name1, inn1, inn_dir1, inn_own1, contact_site, name_dir1, phone_dir1, name_own1, phone_own1 from users where id_eac = {id_}"""
                await cursor.execute(string)
                ans = await cursor.fetchall()
                ans = ans[0]
                inn['link'], inn['name'],  inn['cost'], inn['date'], inn['NAME1'], inn['ИНН_slave1'], inn['ИНН_DIR1'], inn['ИНН_OWN1'], inn['cont_from_page'], inn['ИНН_DIR1_name'], inn['ИНН_DIR1_phone'], inn['ИНН_OWN1_name'], inn['ИНН_OWN1_phone'], inn['counter'] = ans[0], ans[1], ans[2], ans[3], ans[4], ans[5], ans[6].split(', '), ans[7].split(', '), ans[8], ans[9].split('|'), ans[10].split('|'), ans[11].split('|'), ans[12].split('|'), id_
                await conn.commit()
    except Exception as e:
        print(f"Ошибка при экспорте: {e}", select_users2.__name__)
        return False
    return True

async def get_user(id_: str, callback_query: types.CallbackQuery):
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                string = f"""UPDATE users set id_user = {callback_query.from_user.id}, data = CURDATE(), id_message = {callback_query.message.message_id} where id = {id_}"""
                await cursor.execute(string)
                await cursor.fetchall()
                await conn.commit()
    except Exception as e:
        print(f"Ошибка при экспорте: {e}", get_user.__name__)
        return False
    return True

async def check_user(name: str) -> bool:
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                string = f"""select id from users where name = '{name}'"""
                await cursor.execute(string)
                ans = await cursor.fetchall()
                await conn.commit()
                return bool(ans)
    except Exception as e:
        print(f"Ошибка при экспорте: {e}", check_user.__name__)
        return False
