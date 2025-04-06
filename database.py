import aiomysql


async def add_user(id_user: int, id_lead:int, pool:aiomysql.pool.Pool) -> bool:
    string = f'INSERT users(id_user, id_lead, data) VALUES ({id_user}, {id_lead}, CURDATE())'
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

