import os
from playwright.async_api import async_playwright

download_dir = os.path.join(os.getcwd(), r"sovk")
if not os.path.exists(download_dir):
    os.makedirs(download_dir)


async def process_inn(inn: str) -> bool:
    flag = True
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        context = await browser.new_context(accept_downloads=True)
        page = await context.new_page()
        try:
            await page.goto('https://egrul.nalog.ru/')
            await page.fill('input#query', inn)
            await page.click('#btnSearch')
            await page.wait_for_selector('.op-excerpt', timeout=10000)
            await page.click('.op-excerpt')
            async with page.expect_download() as download_info:
                await page.click('.op-excerpt')
                download = await download_info.value
                download_path = os.path.join(download_dir, f"{inn}.pdf")
                await download.save_as(download_path)
        except Exception as e:
            flag = False
        finally:
            await context.close()
            await browser.close()
            return True if flag else False
