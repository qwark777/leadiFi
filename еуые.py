import asyncio
import time
from collections import defaultdict

from playwright.async_api import async_playwright


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

        time.sleep(100)  # Простое решение

        # Или с использованием Playwright (предпочтительно):

        browser.close()



asyncio.run(eac())