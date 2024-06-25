from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

element = []
        
Username = ""
Password = ""

elements = []

display_name = "WAHYU RIDHO"

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome()

login_url = "https://academic.ui.ac.id/main/Authentication/"
homepage = "https://academic.ui.ac.id/main/Welcome/"
logout = "https://academic.ui.ac.id/main/Authentication/Logout"
siak = "https://academic.ui.ac.id/main/CoursePlan/CoursePlanEdit"

def outin():
    driver.get(logout)
    driver.get(login_url)

def login():
    
    driver.execute_script(f"arguments[0].value = '{Username}';", driver.find_element(By.ID, "u"))
    driver.execute_script(f"arguments[0].value = '{Password}';", driver.find_element(By.NAME, "p"))
    driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, "//input[@value='Login']"))
    
def check2():
    for element in elements:
        # antisipasi salah masukkin kode
        try:
            radio_input = driver.find_element(By.XPATH, f"//input[@value='{element}']")
            if(not radio_input.is_selected()): 
                radio_input.click()
            else:
                print(f"sudah dipilih! ()")
        except:
            print(f"tidak ada! (kode: )")
            pass
    button = driver.find_element(By.XPATH, "//input[@value='Simpan IRS']")
    button.click()
        
def check():
    for element in elements:
        try :
            driver.execute_script("arguments[0].checked = 'checked';", driver.find_element(By.XPATH, f"//input[@value='{element}']"))
        except:
            print("salah kode")
            pass
    driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, "//input[@value='Simpan IRS']"))

        

if __name__ == "__main__":    
    war = True
    begin = True
    
    while war:
        
        if begin:
            begin = False
            driver.get(login_url)
        
        if "IRS berhasil tersimpan!" in driver.page_source:
            break
        
        if(driver.current_url != "https://academic.ui.ac.id/main/Welcome/" and not "Magister" in driver.page_source):
            driver.get(login_url)
            continue
        elif(driver.current_url != "https://academic.ui.ac.id/main/Welcome/"):
            login()
        if(not display_name in driver.page_source):
            driver.get(login_url)
            continue
        if("guest" in driver.page_source):
            outin()
            continue
        print("login")
        driver.get(siak)
        if not "Simpan IRS" in driver.page_source:
            print("war is not started")
            outin()
            continue
        check()
        while not "IRS berhasil tersimpan!" in driver.page_source:
            driver.refresh()
            if "Simpan IRS" in driver.page_source:
                check()
            elif "Waspada terhadap pencurian password!" in driver.page_source:
                break
        if "Waspada terhadap pencurian password!" in driver.page_source:
            continue
        break

    print('done')