import asyncio
import re
import time

from playwright.async_api import async_playwright


async def checko(inn: str):
    titles = []
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        page = await browser.new_page()
        await page.goto('https://checko.ru/')
        await page.fill('input#search', str(inn))

        await page.click('button.search-button')
        time.sleep(4)
        list_items = await page.locator("ul.list.list-disc.list-lg.ms-3 > li").all()

        titles = []
        for item in list_items:
            # Получаем текст ссылки внутри li
            link_text = await item.text_content()
            if 'Заключение договора финансовой аренды (лизинга)' in link_text:
                numbers = re.findall(r'\d+', link_text)
                titles.append(int(numbers[-1]))


    await browser.close()
    return sum(titles)
