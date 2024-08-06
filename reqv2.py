from datetime import datetime
import requests
import sys
from time import sleep
from bs4 import BeautifulSoup
import ssl
from urllib3 import poolmanager
import multiprocessing


MAIN_URL = "https://academic.ui.ac.id/main/Authentication/"
LOGIN_URL = "https://academic.ui.ac.id/main/Authentication/Index"
CHANGE_ROLE_URL = "https://academic.ui.ac.id/main/Authentication/ChangeRole"
ISI_IRS_URL = "https://academic.ui.ac.id/main/CoursePlan/CoursePlanEdit"
SAVE_IRS = "https://academic.ui.ac.id/main/CoursePlan/CoursePlanSave"
PAGE = None
headers = {"Content-Type": "application/x-www-form-urlencoded"}


class TLSAdapter(requests.adapters.HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        """Create and initialize the urllib3 PoolManager."""
        ctx = ssl.create_default_context()
        ctx.set_ciphers("DEFAULT@SECLEVEL=1")
        self.poolmanager = poolmanager.PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_version=ssl.PROTOCOL_TLS,
            ssl_context=ctx,
        )

def main():
    USERNAME = "wahyu.ridho"
    PASSWORD = "2424angga4242"
    TERM = "Term 1"
    SUCCESS = False

    if USERNAME is None or PASSWORD is None:
        print("Gagal saat mendapatkan Username dan Password dari File Config")
        sys.exit()
    while not SUCCESS:
        sess = requests.Session()
        sess.mount("https://", TLSAdapter())
        payload = {}
        payload["u"] = USERNAME
        payload["p"] = PASSWORD
        print("Try to login")
        try:
            PAGE = sess.post(LOGIN_URL, data=payload)
        except:
            continue
        if "redirecting..." not in PAGE.text:
            print("Terjadi masalah saat melakukan Login ke Siak")
            print("Retrying...")
            continue
        if "Login Failed" in PAGE.text:
            continue
        while "Mahasiswa" not in PAGE.text:
            try:
                PAGE = sess.get(CHANGE_ROLE_URL)
            except:
                continue
            if "WAHYU RIDHO" in PAGE.text:
                break
        if "WAHYU" not in PAGE.text:
            print("Login gagal")
            continue
        if TERM not in PAGE.text:
            print("war not started")
            print(datetime.now())
            continue
        while True:
            try:
                print("Try to open isi siak page")
                PAGE = sess.get(ISI_IRS_URL)
            except Exception as e:
                print(e)
                continue
            if "WAHYU RIDHO" in PAGE.text:
                break
            if "Waspada terhadap pencurian password!" in PAGE.text:
                break

        if "Simpan IRS" not in PAGE.text:
            print("Gagal dalam membuka halaman Pengisian IRS")
            print("Retrying...")
            print(datetime.now())
            continue

        soup = BeautifulSoup(PAGE.content, "html.parser")

        dummy = {"tokens": 0,
        'c[603183]': '749565',
        'c[603026]': '749564',
        "comment": (None),
        "submit": "Simpan IRS"}

        payload = {"tokens": 0,
        'c[CSIM603183_06.00.12.01-2024]': '754559-3', #Anaperancis A
        'c[CSIM603026_06.00.12.01-2024]': '754562-4', #Apap A
        'c[CSIM603154_06.00.12.01-2024]': '754995-4', #Jarkomdat B
        'c[CSIM102113_06.00.12.01-2024]': '755002-4', #Pengstat D
        'c[CSCE604151_06.00.12.01-2024]': '753931-3', #Sistem Tertanam
        'c[CSCE604133_06.00.12.01-2024]': '754913-3', #Computer Vision
        "comment": (None),
        "submit": "Simpan IRS"}


        token_value = soup.find("input", {"name": "tokens"})["value"]
        payload["tokens"] = token_value
        res = None
        while True:
            try:
                res = sess.post(SAVE_IRS, headers=headers, data=payload)
            except Exception as e:
                print(e)
                # notify_bot(e)
                continue
            if "IRS berhasil tersimpan!" in res.text:
                print("Berhasil tersimpan!")
                # notify_bot("Berhasil tersimpan!")
                break
            if "Waspada terhadap pencurian password!" in res.text:
                print("Terjadi masalah saat melakukan Login ke Siak")
                print("Retrying...")
                break
        if "IRS berhasil tersimpan!" in res.text:
            print("Berhasil tersimpan!")
            print(res.text)
            # notify_bot("Berhasil tersimpan!")
            break
        else:
            print("Retrying...")
            continue


def notify_bot(message):
    import requests
    import json

    url = "https://api.line.me/v2/bot/message/push"
    payload = {
        "to": "Ue758bbf751c8373543408390fd4a5742",
        "messages": [
            {
                "type": "flex",
                "altText": "This is a Flex Message",
                "contents": {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {"type": "text", "text": message},
                        ],
                    },
                },
            }
        ],
    }
    # Adding empty header as parameters are being sent in payload
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 3V/0D9c5sqfM/JvxXcNZFH4PWzhBiFzyWlKVaHf+OxKpGAXzDsx2rmdaMq3i2ewBZwjJRR3pJXb+JPzysMvHM2UDXKv8ao2DYaOZw/KwJeVlaJzIx5KSc/l17aHiR6evZxUGkeFTtdkl/b8Qbz5u2QdB04t89/1O/w1cDnyilFU=",
    }

    r = requests.post(url, data=json.dumps(payload), headers=headers)
    print(r.content)


if __name__ == "__main__":

    # notify_bot('Script dimulai')
    main()
