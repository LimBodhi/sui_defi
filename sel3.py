from selenium import webdriver
from selenium.webdriver.common.by import By
from base64 import b64decode
import json
import datetime
from selenium.webdriver.chrome.options import Options

USERNAME = "wahyu.ridho"
PASSWORD = ""
DISPLAY_NAME = "WAHYU RIDHO"

LOGIN_URL = "https://academic.ui.ac.id/main/Authentication/"
HOMEPAGE_URL = "https://academic.ui.ac.id/main/Welcome/"
LOGOUT_URL = "https://academic.ui.ac.id/main/Authentication/Logout"
COURSE_EDIT_URL = "https://academic.ui.ac.id/main/CoursePlan/CoursePlanEdit"

options = Options()
options.add_experimental_option("detach", True)
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)


courses = [
'740359-3',
'740129-3',
'740142-4',
'740145-3',
'739090-4',
'739110-4',
]



def relogin():

    driver.get(LOGOUT_URL)
    driver.get(LOGIN_URL)


def login():
    driver.execute_script(
        f"arguments[0].value = '{USERNAME}';", driver.find_element(By.ID, "u"))
    driver.execute_script(
        f"arguments[0].value = '{PASSWORD}';", driver.find_element(By.NAME, "p"))
    driver.execute_script("arguments[0].click();", driver.find_element(
        By.XPATH, "//input[@value='Login']"))


def save_course_plan():
    count = 0
    for course in courses:
        try:
            driver.execute_script("arguments[0].checked = 'checked';", driver.find_element(
                By.XPATH, f"//input[@value='{course}']"))
            count += 1
        except Exception as e:
            print()
            info(f"[!] Wrong course for: {course}")
    if count == 0:
        info("[!] No course selected.")
        return False
    driver.execute_script("arguments[0].click();", driver.find_element(
        By.XPATH, "//input[@value='Simpan IRS']"))
    return True


def is_in_login_page():
    return "Waspada terhadap pencurian password!" in driver.page_source


def is_save_course_successful():
    return "IRS berhasil tersimpan!" in driver.page_source

    
def is_course_plan_editable():
    return "Simpan IRS" in driver.page_source


def is_role_student():
    return "Mahasiswa" in driver.page_source


def info(msg):
    print(msg, f"[{datetime.datetime.now()}]")


def try_login():
    if driver.current_url != HOMEPAGE_URL and not is_in_login_page():
        driver.get(LOGIN_URL)
        return False
    elif driver.current_url != HOMEPAGE_URL:
        login()

    if DISPLAY_NAME not in driver.page_source:
        driver.get(LOGIN_URL)
        return False

    if "guest" in driver.page_source:
        relogin()
        return False

    info("[*] Successfully logged in!")
    return True

def is_term():
    if "Term 2" in driver.page_source:
        return True
    return False


def main():
    #load_course_data()
    while True:
        is_logged_in = try_login()
        if not is_logged_in:
            continue
        if not is_term():
            info("[!] War has not started yet. Retrying...")
            relogin()
            continue
        driver.get(COURSE_EDIT_URL)
        while "Pengisian IRS" not in driver.page_source:
            driver.get(COURSE_EDIT_URL)
            info("[*] Trying to save course plan...")
            if is_in_login_page():
                break
        if not is_course_plan_editable():
            info("[!] War has not started yet. Retrying...")
            relogin()
            continue
        if not save_course_plan():
            relogin()
            continue
        while not is_save_course_successful():
            driver.refresh()
            if is_course_plan_editable():
                save_course_plan()
            elif is_in_login_page():
                break
        if is_in_login_page() or driver.current_url == HOMEPAGE_URL:
            continue
        if "Anda tidak memiliki IRS!" in driver.page_source:
            driver.get(LOGIN_URL)
            continue

        break

    info('[+] Done!')
    driver.get("https://academic.ui.ac.id/main/CoursePlan/CoursePlanViewSummary")


if __name__ == "__main__":
    main()
   