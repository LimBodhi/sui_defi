from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
import datetime



Username = "wahyu.ridho"
Password = "2424angga4242"
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'DEFAULT@SECLEVEL=1'
jadwal = "https://academic.ui.ac.id/main/Schedule/Index"
login_data = {
    'u': f"{Username}",
    'p': f"{Password}"
}

login_url = "https://academic.ui.ac.id/main/Authentication/"
session = requests.Session()
response = session.post(login_url, data=login_data, verify=False)
next_page_response = session.get("https://academic.ui.ac.id/main/Authentication/ChangeRole", verify=False)
next_page_response = session.get(jadwal)
next_page_response = session.get("https://academic.ui.ac.id/main/Schedule/Index?period=2024-1&search=", verify=False)

soup = BeautifulSoup(next_page_response.text, 'html.parser')

# Cari elemen <input> dengan atribut name="tokens" dan ambil nilai atribut value-nya

# Menggunakan list comprehension untuk mengambil semua informasi mata kuliah
informasi_matkul_list = []
datasks = []
for th_tag in soup.find_all('th', class_='sub border2 pad2'):
    info = th_tag.contents[0].strip().split(" - ")
    info2 = th_tag.contents[-1].strip().split(";")
    kode_matkul = info[0]
    nama_matkul = th_tag.find('strong').text

    # Cari kurikulum_string yang sesuai dengan format "06.00.12.01-2020"
    kurikulum_string = ""
    for part in info2:
        if "Kurikulum" in part:
            kurikulum_string = part.split("Kurikulum ")[-1].strip()
            break
    for part in info2:
        if "sks" or "SKS" in part:
            sks = part.replace("(", "")
            sks = sks.replace(")", "")
            data = sks.split(" ")
            
            sks = (data[0])
            datasks.append(sks)
            break


    # Mengambil kode kurikulum dengan format "06.00.12.01-2020"

    informasi_matkul_list.append((kode_matkul.strip().replace("-", ""), nama_matkul.strip(), kurikulum_string.strip()))

    
a_tags = soup.find_all('a', href=lambda href: href and '/main/CoursePlan/ClassInfo?cc=' in href)
kode = []
if a_tags:
    a = 0
    for a_tag in a_tags:
        href_value = a_tag['href']
        cc_value = href_value.split('=')[-1]
        kode.append(cc_value.strip())
        a += 1
else:
    print("Tidak ditemukan.")
# Cetak semua informasi mata kuliah
x = 0
file = open("data.txt", "w")
for kode_matkul, nama_matkul, kode_kurikulum  in informasi_matkul_list:
    file.write(f"Nama mata kuliah: {nama_matkul}\n")
    file.write(f"Kode mata kuliah: c[{kode_matkul.strip()}_{kode_kurikulum.strip()}]\n")
    file.write(f"SKS: {datasks[x]}\n")
    file.write("\n")
    x += 1
file.close()
