import asyncio
import time

from playwright.async_api import async_playwright


async def checko(inn: int):
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        page = await browser.new_page()
        await page.goto('https://checko.ru/')
        await page.fill('input#search', str(inn))

        await page.click('button.search-button')
        time.sleep(4)
    await browser.close()
asyncio.run(checko(7717771440))