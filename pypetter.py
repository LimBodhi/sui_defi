import asyncio
from pyppeteer import launch
import datetime

USERNAME = 'wahyu.ridho'
PASSWORD = 'Angga2005'
courses = []

async def main():

    browser = await launch()
    page = await browser.newPage()

    while True:

        await page.goto('https://academic.ui.ac.id/main/Authentication/')
        
        try:
            await login(page)
        except:
            continue

        await page.waitForNavigation()
        await page.goto('https://academic.ui.ac.id/main/Authentication/ChangeRole')
        
        try:
            if "WAHYU RIDHO" in await page.content():
                print("login berhasil")
            else:
                continue
            if "Term 2" not in await page.content:
                await outin(page)
                print(datetime.datetime.now())
                continue
            await page.goto("https://academic.ui.ac.id/main/CoursePlan/CoursePlanEdit")
            if "Simpan IRSi" not in await page.content:
                await outin(page)
                print(datetime.datetime.now())
                continue
            await check(page)
            await page.waitForNavigation()
            if "IRS berhasil tersimpan!" not in await page.content: 
                await outin(page)
                print(datetime.datetime.now())
                continue
            print("done")
            break
            
            
        except:
            continue
    

async def login(page):

    await page.evaluate(f"() => {{ document.querySelector('#u').value = '{USERNAME}'; }}")
    await page.evaluate(f"() => {{ document.querySelector('[name=p]').value = '{PASSWORD}'; }}") 
    await page.evaluate(f"() => {{ document.querySelector(\"input[value='Login']\").click(); }}")

async def check(page):

    for course in courses:
        try:
            await page.evaluate(f"() => {{ document.querySelector(\"input[value='{course['id']}']\").checked = true; }}")
        except Exception as e:
            print(e)
            print()
            print(f"[!] Wrong course for: {course}")
    await page.evaluate(f"() => {{ document.querySelector(\"input[value='Simpan IRS']\").click(); }}")

async def outin(page):
    await page.goto('https://academic.ui.ac.id/main/Authentication/Logout')
    await page.goto('https://academic.ui.ac.id/main/Authentication/')



asyncio.get_event_loop().run_until_complete(main())