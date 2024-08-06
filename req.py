import requests
import datetime
from lxml import html
from bs4 import BeautifulSoup
from time import sleep
import certifi
import warnings

warnings.filterwarnings("ignore")

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

SEMESTER = "Term 1"

headers = {"Content-Type": "application/x-www-form-urlencoded"}

data = {"tokens": 0,
        'c[603183]': '749565',
        'c[603026]': '749564',
        "comment": (None),
        "submit": "Simpan IRS"}


# Membuat sesi (session)
# Cek apakah login berhasil dengan memeriksa respons atau URL setelah login

while True:
	session = requests.Session()
	try:
		print("masuk")
		response = session.post(login_url, data=login_data, verify=False)
		print("sending login")
	except Exception as e:
		print(e)
		continue
	if "redirecting..." not in response.text:
		print("Terjadi masalah saat melakukan Login ke Siak")
		print("Retrying...")
		continue
	if "Login Failed" in response.text:
		continue
	try:
		next_page_response = session.get("https://academic.ui.ac.id/main/Authentication/ChangeRole", timeout=2, verify=False)
	except:
		continue
	while "Mahasiswa" not in next_page_response.text:
		try:
			next_page_response = session.get("https://academic.ui.ac.id/main/Authentication/ChangeRole", verify=False)
		except:
			continue
	if not "WAHYU RIDHO" in next_page_response.text or "guest" in next_page_response.text:
		print("down")
		print(datetime.datetime.now())
		continue
	print("Login berhasil.")
	if SEMESTER in next_page_response.text: #cek semester udah ganti apa belum
		while True:
			try:
				next_page_response = session.get(siak, verify=False)
			except:
				continue
			if "Simpan IRS" in next_page_response.text:
				break
			if "Waspada terhadap pencurian password!" in next_page_response.text:
				break
	else:
		print("war not started")
		#print time now
		print(datetime.datetime.now())
		continue
	if "Waspada terhadap pencurian password!" in next_page_response.text:
		continue
	print("war started")
	soup = BeautifulSoup(next_page_response.content, "html.parser")
	tokens_value = soup.find("input", {"name": "tokens"})["value"]
	data["tokens"] = tokens_value
	while True:
		try:
			response = session.post(url, headers=headers, data=data, verify=False)
		except:
			continue
		if "IRS berhasil tersimpan!" in response.text:
			print(""" done banh """)
			break
		elif "Waspada terhadap pencurian password!" in response.text:
			break
		else:
			continue
	if "Waspadalah terhadap pencurian password!" in response.text:
		print("down")
		print(datetime.datetime.now())
		continue
	
	break

print("done banh")
print(datetime.datetime.now())

