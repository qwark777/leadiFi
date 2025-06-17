from collections import defaultdict
from datetime import datetime

from aiogram import Router, types, Bot, F
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from playwright.async_api import async_playwright

from database import export_mysql_to_excel
from info import users, User, admins
from main import process_user
from tg import get_one_user

admins_router = Router()
global bot
async def create_admins_router(bt: Bot):
    global bot
    bot = bt


@admins_router.message(StateFilter(None), Command("data"))
async def execl(message: types.Message, state: FSMContext):
    if message.from_user.id not in admins:
        return
    if await export_mysql_to_excel():
        await bot.send_document(message.chat.id, types.FSInputFile(path="data.xlsx"))
    else:
        await bot.send_message(message.chat.id, 'Файл утерялся @qwark666')

@admins_router.message(StateFilter(None), Command("test"))
async def test(message: types.Message, state: FSMContext):
    if message.from_user.id not in admins:
        return
    await bot.send_message(message.chat.id, "Отправь ссылку")
    await state.set_state(User.test)

inn = defaultdict(lambda : defaultdict(lambda : '-'))
@admins_router.message(User.test, F.text)
async def test_2(message: types.Message, state: FSMContext):
    if message.from_user.id not in admins:
        return
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        new_page = await browser.new_page()
        await new_page.goto(message.text)
        await new_page.wait_for_load_state('networkidle')
        close_button = await new_page.wait_for_selector('.btn-close.closePopUp', timeout=5000)
        await close_button.click()

        await new_page.wait_for_selector('.blockInfo__section section', timeout=10000)
        sections = await new_page.query_selector_all('.blockInfo__section section')
        inn_element = await new_page.query_selector('span.grey-main-light + span')
        inn_slave = await inn_element.inner_text()
        for section in sections:
            title_element = await section.query_selector('.section__title')
            info_element = await section.query_selector('.section__info')

            if title_element and info_element:
                title = await title_element.inner_text()
                info = await info_element.inner_text()
                if title == 'ИНН':
                    inn[inn_slave]['inn_owner'] = info

        name = await new_page.query_selector('.cardMainInfo__content .text-break.d-block')
        name = await name.inner_text()
        if 'Посмотреть все' in name:
            name = name[:name.find('Посмотреть все')]

        date_container = await new_page.query_selector('div.date.mt-auto')
        sections = await date_container.query_selector_all('div.cardMainInfo__section')
        section = sections[-1]

        date_str = (await (await section.query_selector('span.cardMainInfo__content')).inner_text()).strip()
        date_obj = datetime.strptime(date_str, "%d.%m.%Y")
        inn[inn_slave]['date'] = str(date_obj.date())

        cells = await new_page.locator("tr.tableBlock__row td.tableBlock__col").all()
        for index, cell in enumerate(cells, 1):
            cell_text = (await cell.inner_text()).strip()
            if cell_text and '@' in cell_text:
                inn[inn_slave]['cont_from_page'] = cell_text.replace('\n', ' ')

        inn[inn_slave]['name'] = name
        await new_page.close()
        await process_user(inn_slave)


@admins_router.message(StateFilter(None), Command("find"))
async def start(message: types.Message, state: FSMContext):
    if message.from_user.id not in users:
        return
    await bot.send_message(message.chat.id, "Отправьте ИНН")
    await state.set_state(User.find)


@admins_router.message(User.find, F.text)
async def find(message: types.Message, state: FSMContext):
    if message.from_user.id not in users:
        return
    try:
        int(message.text)
    except ValueError:
        await message.answer('Неправильный формат')
        await state.clear()
    if len(message.text) == 10:
        await process_user(message.text, 2, message.from_user.id)
        await state.clear()
    elif len(message.text) == 12:
        await get_one_user(message.text, bot, message.from_user.id)
        await state.clear()
    else:
        await message.answer('Неправильный формат')
        await state.clear()