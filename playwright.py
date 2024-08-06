from playwright.sync_api import sync_playwright
import datetime
import sys

#username dan password siak ng untuk login
username = ''
password = ''


#data matkul yang ingin kalian ambil
#data matkul terdapat pada name di html jadwal kuliah + jumlah sks      
elements = ['717633-4']

with sync_playwright() as p:
    #memakai chrome sebagai browser
    def login():
        username_field = page.wait_for_selector("#u")
        page.evaluate(f"document.querySelector('#u').value = '{username}'", username_field)

        password_field = page.wait_for_selector("input[name='p']")
        a = ('input[name="p"]')
        page.evaluate(f"document.querySelector('{a}').value = '{password}'", password_field)
        page.click("input[value='Login']")
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    while True:
        #masuk ke web siak dan memasukkan username serta password dan login
        page.goto("https://academic.ui.ac.id/main/Authentication/")
        username_field = page.wait_for_selector("#u")
        page.evaluate(f"document.querySelector('#u').value = '{username}'")

        password_field = page.wait_for_selector("input[name='p']")
        a = ('input[name="p"]')
        page.evaluate(f"document.querySelector('{a}').value = '{password}'")
        page.evaluate("arguments[0].click();", ("input[value='Login']"))
        #masuk ke web courseplanedit
        if 'WAHYU RIDHO' in page.content():
            print('masuk berhasil')
        #antisipasi untuk web siak down
        elif 'guest' in page.content():
            print('masuk gagal')
            page.goto("https://academic.ui.ac.id/main/Authentication/Logout")
            continue
        else:
            print('masuk gagal')
            page.goto("https://academic.ui.ac.id/main/Authentication/Logout")
            continue
        #antisipasi jika siak war belum dimulai
        page.goto('https://academic.ui.ac.id/main/CoursePlan/CoursePlanEdit')
        if 'Simpan IRS' not in page.content():
            print('belum war')
            print(datetime.datetime.now())
            page.goto("https://academic.ui.ac.id/main/Authentication/Logout")
            continue
        else:
            #memilih matkul jika siak war sudah dimulai
            for element in elements:
                a = f'input[value="{element}"]'
                password_field = page.wait_for_selector(f'{a}')
                page.evaluate(f"document.querySelector('{a}').checked = 'checked'", password_field)
            page.click("input[value='Simpan IRS']")
        if 'IRS berhasil tersimpan!' in page.content():
                print('war berhasil')
                break
        else:
            page.goto("https://academic.ui.ac.id/main/Authentication/Logout")
            continue
            #antisipasi jika siak down saat simpan irs
            '''while not 'IRS berhasil tersimpan!' in page.content():
                print('ulang')
                page.refresh()
                if 'Simpan IRS' in page.content():
                    for element in elements:
                        a = f'input[value="{element}"]'
                        password_field = page.wait_for_selector(f'{a}')
                        page.evaluate(f"document.querySelector('{a}').checked = 'checked'", password_field)
                        
                    page.click("input[value='Simpan IRS']")'''
            
               
    page.pause()
