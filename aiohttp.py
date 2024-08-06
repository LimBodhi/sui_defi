import asyncio
import aiohttp
from bs4 import BeautifulSoup
import ssl
from datetime import datetime
import warnings

warnings.filterwarnings("ignore", category=ResourceWarning)

MAIN_URL = "https://academic.ui.ac.id/main/Authentication/"
LOGIN_URL = "https://academic.ui.ac.id/main/Authentication/Index"
CHANGE_ROLE_URL = "https://academic.ui.ac.id/main/Authentication/ChangeRole"
ISI_IRS_URL = "https://academic.ui.ac.id/main/CoursePlan/CoursePlanEdit"
SAVE_IRS = "https://academic.ui.ac.id/main/CoursePlan/CoursePlanSave"
RINGKASAN_URL = "https://academic.ui.ac.id/main/CoursePlan/CoursePlanSummary"

USERNAME = ""
PASSWORD = ""
TERM = "Term 1"
SAVEDTEXT = ""

async def login(session):
    payload = {"u": USERNAME, "p": PASSWORD}
    async with session.post(LOGIN_URL, data=payload) as response:
        text = await response.text()
        if "redirecting..." not in text:
            print("Terjadi masalah saat melakukan Login ke Siak")
            return False
        if "Login Failed" in text:
            return False
    return True

async def change_role(session):
    global SAVEDTEXT
    async with session.get(CHANGE_ROLE_URL) as response:
        text = await response.text()
        if "WAHYU RIDHO" not in text and "Mahasiswa" not in text:
            print("Gagal dalam mengganti role")
            return False
        SAVEDTEXT = text
    return True

async def get_siak_page(session):
    async with session.get(ISI_IRS_URL) as response:
        text = await response.text()
        if "Pengisian IRS" not in text:
            print("Gagal dalam membuka halaman Pengisian IRS")
            return False
        return text

async def fill_irs(session, payload):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}     
    async with session.post(SAVE_IRS, headers=headers, data=payload) as response:
        text = await response.text()
        if "IRS berhasil tersimpan!" in text:
            print("Berhasil tersimpan!")
            return True
        else:
            print("Gagal menyimpan IRS")
            return False

async def get_ringkasan(session):
    async with session.get(RINGKASAN_URL) as response:
        text = await response.text()
        if "Ringkasan" not in text:
            print("Gagal membuka halaman Ringkasan Pengisian IRS")
            return False
        print("Berhasil")
        return text

async def main():
    while True:
        ssl_context = ssl.create_default_context()
        ssl_context.set_ciphers("DEFAULT@SECLEVEL=1")
        connector = aiohttp.TCPConnector(ssl=ssl_context)
        session = aiohttp.ClientSession(connector=connector)
        try:
            print("Try to login")
            if not await login(session):
                print("Login failed. Retrying...")
                await session.close()
                continue
            while not await change_role(session):
                print("Failed to change role. Retrying...")
                continue
            if TERM not in SAVEDTEXT:
                print(f"War not started {datetime.now()}")
                await session.close()
                continue
            while True:
                print("Try to open isi siak page")
                text = await get_siak_page(session)
                if not text:
                    print("Failed to open isi siak page. Retrying...")
                    continue
                break
            soup = BeautifulSoup(text, "lxml")
            token_value = soup.find("input", {"name": "tokens"})["value"]
            
            payload = {
                "tokens": token_value,
                'c[CSGE602012_01.00.12.01-2020]': '724680-3',
                'c[CSGE602091_01.00.12.01-2020]': '724707-3',
                'c[CSGE602022_01.00.12.01-2020]': '724720-4',
                'c[CSGE602040_01.00.12.01-2020]': '724748-4',
                'c[CSIM602155_01.00.12.01-2020]': '725467-3',
                "comment": None,
                "submit": "Simpan IRS"
            }

            print("Try to fill IRS")
            while True:
                if not await fill_irs(session, payload):
                    print("Failed to fill IRS. Retrying...")
                    continue
                break
            
            await get_ringkasan(session)
            
        except Exception as e:
            print(f"Error: {e}")
            continue

if __name__ == "__main__":
    asyncio.run(main())
