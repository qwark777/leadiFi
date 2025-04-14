async def potom():
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

async def subprocess(bot: Bot):
    for i in inn.keys():
        if await pdf_parcer1(fr"C:\sovk\{i}.pdf", inn[i]) and await pdf_parcer2(fr"C:\sovk\{inn[i]['inn_owner']}.pdf", inn[i]):
            pass
        else:
            print(f'Lost file{i}')
    for i in inn.keys():
        await print_form(i, bot)


async def print_form(i: int):
    stri = pattern
    global counter
    counter += 1
    await bot.send_message(Admin.id_ivan_id,
                           stri.format(i=counter, link=inn[i]['link'], name=inn[i]['name'], cost=inn[i]['cost'],
                                       date=inn[i]['date'], inn_owner=inn[i]['inn_owner'],
                                       i_dir2=inn[i]['ИНН_DIR2'], i_own2=', '.join(inn[i]['ИНН_OWN2']),
                                       inn_slave=i, i_dir1=inn[i]['ИНН_DIR1'], i_own1=', '.join(inn[i]['ИНН_OWN1']),
                                       cont_from_page=inn[i]['cont_from_page']), parse_mode="HTML")
