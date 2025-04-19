import asyncio
from collections import defaultdict
from datetime import datetime
from playwright.async_api import async_playwright
prev_link = "https://zakupki.gov.ru"

async def eac():
    inn = defaultdict(lambda : defaultdict(lambda : '-'))
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        page = await browser.new_page()
        await page.goto('http://zakupki.gov.ru/epz/contract/search/results.html')
        await page.wait_for_load_state('networkidle')
        close_button = await page.wait_for_selector('.btn-close.closePopUp', timeout=5000)
        await close_button.click()

        await page.wait_for_selector('label.params-text', timeout=10000)
        buttons = await page.query_selector_all('label.params-text')
        await buttons[1].click()
        await page.click('input#contractPriceFrom')
        await page.fill('input#contractPriceFrom', '100000000')
        await page.wait_for_selector('#btn-floating button.btn.btn-primary', timeout=10000)
        button = await page.query_selector('#btn-floating button.btn.btn-primary')
        await button.click()
        await page.wait_for_selector('span.dropdown__text_selected', timeout=10000)

        await page.click('span.dropdown__text_selected')

        await page.wait_for_selector('li.dropdown-list__item-normal', timeout=10000)

        await page.click('li[type="PUBLISH_DATE"].dropdown-list__item-normal')


        await page.wait_for_selector('.registry-entry__header-mid__number a', timeout=10000)
        for j in range(3):
            await page.wait_for_selector('.registry-entry__header-mid__number a', timeout=10000)
            links = await page.query_selector_all('.registry-entry__header-mid__number a')
            price = await page.query_selector_all('.price-block__value')
            for i, link in enumerate(links):
                try:
                    cost = price[i]
                    linki = await link.get_attribute('href')
                    async with page.expect_popup() as popup_info:
                        await link.click()
                    new_page = await popup_info.value
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
                    section=sections[-1]

                    date_str = (await (await section.query_selector('span.cardMainInfo__content')).inner_text()).strip()
                    date_obj = datetime.strptime(date_str, "%d.%m.%Y")
                    inn[inn_slave]['date'] = str(date_obj.date())


                    cells = await new_page.locator("tr.tableBlock__row td.tableBlock__col").all()
                    for index, cell in enumerate(cells, 1):
                        cell_text = (await cell.inner_text()).strip()
                        if cell_text and '@' in cell_text:
                            inn[inn_slave]['cont_from_page'] = cell_text.replace('\n', ' ')

                    inn[inn_slave]['name'] = name
                    inn[inn_slave]['link'] = prev_link + linki
                    inn[inn_slave]['cost'] = await cost.inner_text()
                    await new_page.close()

                except Exception as e:
                    print(e)
            await page.click('a.paginator-button-next')
    await browser.close()
    return inn

