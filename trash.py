# async def potom():
#     for i in inn.keys():
#         if not await process_inn(i):
#             await subprocess(bot)
#             await asyncio.sleep(60)
#             await process_inn(i)
#         if not await process_inn(inn[i]['inn_owner']):
#             await subprocess(bot)
#             await asyncio.sleep(60)
#             await process_inn(inn[i]['inn_owner'])
#     await subprocess(bot)
#
# async def subprocess(bot: Bot):
#     for i in inn.keys():
#         if await pdf_parcer1(fr"C:\sovk\{i}.pdf", inn[i]) and await pdf_parcer2(fr"C:\sovk\{inn[i]['inn_owner']}.pdf", inn[i]):
#             pass
#         else:
#             print(f'Lost file{i}')
#     for i in inn.keys():
#         await print_form(i, bot)
#
#
# async def print_form(i: int):
#     stri = pattern
#     global counter
#     counter += 1
#     await bot.send_message(Admin.id_ivan_id,
#                            stri.format(i=counter, link=inn[i]['link'], name=inn[i]['name'], cost=inn[i]['cost'],
#                                        date=inn[i]['date'], inn_owner=inn[i]['inn_owner'],
#                                        i_dir2=inn[i]['ИНН_DIR2'], i_own2=', '.join(inn[i]['ИНН_OWN2']),
#                                        inn_slave=i, i_dir1=inn[i]['ИНН_DIR1'], i_own1=', '.join(inn[i]['ИНН_OWN1']),
#                                        cont_from_page=inn[i]['cont_from_page']), parse_mode="HTML")
import asyncio

import pdfplumber


async def pdf_parcer2(pdf_path: str) -> bool:
    try:
        with pdfplumber.open(pdf_path) as pdf:
            name = ''
            module = 0
            for page in pdf.pages:
                text = page.extract_text()
                lines = text.split('\n')
                for line in lines:
                    if line == 'Настоящая выписка содержит сведения о юридическом лице':
                        module = 3
                        continue
                    if line == 'полное наименование юридического лица':
                        module = 0
                        continue

                    if module == 3:
                        name += line + ' '
            print(name)


    except:
        pass
await bt.send_message(Admin.id_chat_users,
                           stri.format(i=counter, link=inn['link'], name=inn['name'], cost=inn['cost'],
                                       date=inn['date'], inn_owner=inn['inn_owner'],
                                       i_dir2=inn['ИНН_DIR2'], i_own2=', '.join(inn['ИНН_OWN2']),
                                       i_con_dir2=inn['ИНН_DIR2_contacts'][0] +  str(inn['ИНН_DIR2_contacts'][1]),
                                       i_con_own2= '| '.join(list(inn['ИНН_OWN2_contacts'])),
                                       inn_slave=i, i_dir1=inn['ИНН_DIR1'], i_own1=', '.join(inn['ИНН_OWN1']),
                                       cont_from_page=inn['cont_from_page'],
                                       i_con_dir1=inn['ИНН_DIR1_contacts'][0]  + str(inn['ИНН_DIR1_contacts'][1]),
                                       i_con_own1= inn['ИНН_DIR1_contacts'][0]), parse_mode="HTML",
                           reply_markup=keyboard1)