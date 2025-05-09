from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class Admin:
    time_schedule = 5
    id_chat_bot = -1002406858766
    id_chat_users = -1002261631821
    id_ivan_id = 1188056958
    id_alex_chat = 5201640740
    test_chat = -1002377574530

users = [753407063, 5201640740, 1188056958]
admins = [5201640740, 1188056958]

class User(StatesGroup):
    find = State()


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
find_keyboard = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text="Юридическое", callback_data="btn_3_01"),
            InlineKeyboardButton(text="Физическое", callback_data="btn_3_02")
        ]
    ]
)