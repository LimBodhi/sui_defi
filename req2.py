import requests
import datetime
from lxml import html
import threading
import multiprocessing
from multiprocessing import Pool
from bs4 import BeautifulSoup
from time import sleep


requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'DEFAULT@SECLEVEL=1'
login_url = "https://academic.ui.ac.id/main/Authentication/"
homepage = "https://academic.ui.ac.id/main/Welcome/"
logout = "https://academic.ui.ac.id/main/Authentication/Logout"
siak = "https://academic.ui.ac.id/main/CoursePlan/CoursePlanEdit"
tes = "https://academic.ui.ac.id/main/Academic/HistoryByTerm"
homepage = "https://academic.ui.ac.id/main/Welcome/"
url = "https://academic.ui.ac.id/main/CoursePlan/CoursePlanSave"

login_data = {
    'u': "wahyu.ridho",
    'p': "2424angga4242"
}

headers = {"Content-Type": "application/x-www-form-urlencoded"}

data = {"tokens": 0,
        'c[CSGE602012_01.00.12.01-2020]': '724680-3',
        'c[CSGE602091_01.00.12.01-2020]': '724707-3',
        'c[CSGE602022_01.00.12.01-2020]': '724720-4',
        'c[CSGE602040_01.00.12.01-2020]': '724748-4',
        'c[CSIM602155_01.00.12.01-2020]': '725467-3',
        "comment": (None),
        "submit": "Simpan IRS"}
a = 0
done = True

def perform_http_request(login_data, data, thread_num, headers):
    while done:
        session = requests.Session()
        try:
            response = session.post(login_url, data=login_data, timeout=2)
        except:
            session.close()
            continue
        try:
            next_page_response = session.get("https://academic.ui.ac.id/main/Authentication/ChangeRole", timeout=2)
        except:
            session.close()
            continue
        if not "WAHYU RIDHO" in next_page_response.text or "guest" in next_page_response.text:
            print(f"down")
            session.close()
            continue
        print(f"Login berhasil.")
        try:
            next_page_response = session.get(siak, timeout = 2)
        except:
            session.close()
            continue
        if "Simpan IRS" not in next_page_response.text:
            print(f"belum war")
            print(datetime.datetime.now())
            session.close()
            continue
        else:
            print("war started")
            soup = BeautifulSoup(next_page_response.content, "html.parser")
            tokens_value = soup.find("input", {"name": "tokens"})["value"]
            data["tokens"] = tokens_value
            try:
                response = session.post("https://academic.ui.ac.id/main/CoursePlan/CoursePlanSave", headers=headers, data=data, timeout=0.5)
            except:
                session.close()
                continue
            
        if "IRS berhasil tersimpan!" in response.text:
            print(f"Thread {thread_num}: Berhasil tersimpan!")
            session.close()
            break
        else:
            print(f"Thread {thread_num}: Gagal menyimpan.")
            session.close()
            continue
    print("done banh")

if __name__ == '__main__':   
    processes = []
    for i in range(1, 16):
        process = multiprocessing.Process(target=perform_http_request, args=(login_data, data, i, headers))
        process.start()
        processes.append(process)

    for process in processes:
        process.join(timeout=1)
    

    print(datetime.datetime.now())


