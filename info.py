from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class Admin:
    time_schedule = 5
    id_chat_bot = -1002406858766
    id_chat_users = -1002261631821
    id_ivan_id = 1188056958
    id_alex_chat = 5201640740


pattern_for_group = '''<b>❗Найден новый lead №{i}❗44-ФЗ/94-ФЗ</b>
<b>C сайта ЕАС/контракты</b>
<a href="{link}">Ссылка на контракт </a>
<b>Объект закупки: {name}</b>
<b>Стоимость контракта {cost}</b>
<b>Дата контракта {date}</b>
<b>-------------------------------</b>
<b>ИНН компании заказчика <code>{inn_owner}</code></b>
<b>ИНН лица 'ИПБДДОИЮЛ' <code>{i_dir2}</code></b>
<b>ИНН учредителей <code>{i_own2}</code></b>
<b>Контакты лица 'ИПБДДОИЮЛ' {i_con_dir2}</b>
<b>Контакты учредителей {i_con_own2}</b>
<b>-------------------------------\n</b>
<b>-------------------------------</b>
<b>ИНН компаниии исполнителя <code>{inn_slave}</code></b>
<b>ИНН лица 'ИПБДДОИЮЛ' <code>{i_dir1}</code></b>
<b>ИНН учредителей <code>{i_own1}</code></b>
<b>Контакты с сайта 'ИПБДДОИЮЛ' {cont_from_page}</b>
<b>Контакты лица 'ИПБДДОИЮЛ' {i_con_dir1}</b>
<b>Контакты учредителей {i_con_own1}</b>
<b>-------------------------------</b>
'''

keyboard1 = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text="Забираю ☑️", callback_data="btn_1_01")
        ]
    ]
)


keyboard2 = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text="✅", callback_data="btn_1_02"),
            InlineKeyboardButton(text="Назад 🔙", callback_data="btn_1_03")
        ]
    ]
)
keyboard3 = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text="✅", callback_data="btn_2_01"),
            InlineKeyboardButton(text="❌", callback_data="btn_2_02")
        ]
    ]
)