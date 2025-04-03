import asyncio

from playwright.async_api import async_playwright
from selenium.webdriver.common.devtools.v85.runtime import await_promise


async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        page = await browser.new_page()
        await page.goto('http://zakupki.gov.ru/epz/contract/search/results.html')
        await page.wait_for_load_state('networkidle')
        close_button = await page.wait_for_selector('.btn-close.closePopUp', timeout=5000)
        await close_button.click()
        await page.wait_for_selector('span.dropdown__text_selected', timeout=10000)

        await page.click('span.dropdown__text_selected')

        await page.wait_for_selector('li.dropdown-list__item-normal', timeout=10000)

        await page.click('li[type="PUBLISH_DATE"].dropdown-list__item-normal')



        await asyncio.sleep(50)

    await browser.close()


asyncio.run(main())
