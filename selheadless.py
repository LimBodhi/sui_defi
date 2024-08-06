#Angganion
#2022


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import datetime
        

options = Options()
options.add_argument('--disable-gpu')
options.add_argument('--disable-extensions')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-infobars')
options.add_argument('--disable-notifications')
options.add_argument('--disable-popup-blocking')
options.add_argument('--disable-translate')
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--log-level=3')
options.add_argument('--silent')
options.add_argument('--disable-browser-side-navigation')
driver = webdriver.Chrome(options=options)
#driver = webdriver.Chrome()

login_url = "https://academic.ui.ac.id/main/Authentication/"
homepage = "https://academic.ui.ac.id/main/Welcome/"
logout = "https://academic.ui.ac.id/main/Authentication/Logout"
siak = "https://academic.ui.ac.id/main/CoursePlan/CoursePlanEdit"

USERNAME = ""
PASSWORD = ""

elements = []

DISPLAY_NAME = ""

def outin():
    
    driver.get(logout)
    driver.get(login_url)

def login():
  
    driver.execute_script(
        f"arguments[0].value = '{USERNAME}';", driver.find_element(By.ID, "u"))
    driver.execute_script(
        f"arguments[0].value = '{PASSWORD}';", driver.find_element(By.NAME, "p"))
    driver.execute_script(
        "arguments[0].click();", driver.find_element(By.XPATH, "//input[@value='Login']"))
    
def login2():

    login_script = f'''
        function login() {{
            const usernameInput = document.querySelector("input#u");
            const passwordInput = document.querySelector("input[name=p]");
            const loginButton = document.querySelector("input[value='Login']");

            usernameInput.value = "{USERNAME}";
            passwordInput.value = "{PASSWORD}";
            loginButton.click();
        }}
        login();
    '''

    driver.execute_script(login_script)
def login3():
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "u")))
    element.clear()

# Send the username or text input to the input field
    element.send_keys("")

    #password
    element2 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "p")))
    element2.clear()

# Send the username or text input to the input field
    element2.send_keys("")
   
    driver.find_element(By.XPATH, "//input[@value='Login']").click()
    
def check2():
    for element in elements:
        # antisipasi salah masukkin kode
        try:
            radio_input = driver.find_element(By.XPATH, f"//input[@value='{element}']")
            if(not radio_input.is_selected()): 
                radio_input.click()
            else:
                print(f"sudah dipilih")
        except:
            print(f"tidak ada!")
            pass
    button = driver.find_element(By.XPATH, "//input[@value='Simpan IRS']")
    button.click()
        
def check():
    
    for element in elements:
        try :
            driver.execute_script("arguments[0].checked = 'checked';", driver.find_element(
                By.XPATH, f"//input[@value='{element}']"))
        except:
            print("salah kode")
            pass
    print("kelar milih")
    driver.execute_script("arguments[0].click();", driver.find_element(
        By.XPATH, "//input[@value='Simpan IRS']"))

        

if __name__ == "__main__":    
    war = True
    begin = True
    
    while war:
        
        if begin:
            begin = False
            driver.get(login_url)
            
        if(driver.current_url != "https://academic.ui.ac.id/main/Welcome/" and \
            not "Magister" in driver.page_source):
            print("ulang")
            driver.get(login_url)
            continue
        elif(driver.current_url != "https://academic.ui.ac.id/main/Welcome/"):
            login()
        if(not DISPLAY_NAME in driver.page_source):
            if("guest" in driver.page_source):
                print("guest")
                outin()
                continue
            print("down")
            driver.get(login_url)
            continue
        if("guest" in driver.page_source):
            print("guest")
            outin()
            continue
        print("login")
        driver.get(siak)
        if not "Simpan IRS" in driver.page_source:
            print("war is not started")
            print(datetime.datetime.now())
            outin()
            continue
        print("war")
        check()
        while not "IRS berhasil tersimpan!" in driver.page_source:
            driver.refresh()
            if "Simpan IRS" in driver.page_source:
                check()
            elif "Waspada terhadap pencurian password!" in driver.page_source:
                break
        if "Waspada terhadap pencurian password!" in driver.page_source or \
            driver.current_url == "https://academic.ui.ac.id/main/Welcome/":
            continue
        if "Anda tidak memiliki IRS!" in driver.page_source:
            driver.get(login_url)
            continue
        break

    print("""
                                                                               
          ,KWWWWNXNOc.      .oKWWXd.   ,dd0Wk.    .cl.    lNMMMMMWWMWWWo        
          cNMW0o,'xMNd.   .:KNNOckNk,    'kWNl.   ,0Xc    :XMWkodoloddd'        
          oMMK;   lNWNl  .lXWWk. ,KWk,   .OMWNo.  cNMd.   lWMN:     ...         
         .kWW0,   cNWMx. cXWW0,  .oWWx.  ,0WWWNd. oWMO.  .xWWNc                 
         ,0WW0'   lWMMO..OMMNl    :XMNc  'OWWWWNo.oWWX;  .kMMWOlldxkkOd;.       
         ;XMMK,  .xMMMO':NWW0,    ;KMMx. ;XWWWNWNxkNMNl  ,0WMMWWMMWNNWW0'       
         cNMMX;  ;KWMMk.cWMMk.    ;KWMk. cWWWNxkWWNWMWd. '0MMMXxoc;,:oko        
         cXWMNc 'kWWMNc :XWMk.    :XWWk. lWWMNl,kWWMMWO. '0MWWx.     .;'        
         :XWWWOd0WWWWO' 'OWWO'   .dWWWo  lWWMWd.'OWWWMO' 'OMMMk'.....           
         ;XMWWWWWWWX0l.  ,0MWk;';dXWWK;  cNWWMd  ,ONWM0' '0WWMN0000K0ko;        
         cNMWWWNXOl'::    ,kXWNXNWNOxc.  'OWWNl   'kNWX; :KWWWMMMWMMWWW0,       
         .ok0Ko''' '      ,ldk0Kl.,,    'dO0c    .c0N: .,o0OxxddocckXo.       
                        
                                                                                          
      .cddOKXNKd.         ;0XO;        ,oodkc      ..      lK0c      .oKo.       
      ,0WW0kKWWWo        .xWMWO        .cd0WK;    .dk,    .kMM0     OMK,       
      lNMO;lXMWNc       .lNWWWWo.      .,xWWO,   ;KWl    ;KMWK;     :XWNc       
     .dWWklKWWWk.       :KWNOOWK,      .:kWMM0;  lWMk.   cWMMK;     cWMWo       
     .kMWNNWWNk.       'OWMk.lWWl      .lOMWWW0; lWMK,   oWMMX;     cNMMx.      
     .OMWMMWWNo.      .dWMNc ;XWk.     'o0MMWWW0;lWMNc  .xMWWKc.,:clOWMMKo,.    
     OMWMW0kKN0l.    :XWWO. .kMX:     ;0KWMN0XW00WWWd. .kMWWWXKNWWMMMMMNOo,    
     :KWWXd. dMMWd.  .kWWWk;;l0WWKo:.  cXXWMNolXMWWMMk' 0WMMWKOkdoo0MMMx.,'    
    ,0WWNo  ,0WWWO.  cNMWMWNNNXWWNko,  :KNMMWo.lNWWWMO. ;KWMM0;.    lMMMx...    
    ;k0MX:.:0NMMNd. .kWW0dl;,',xWNl.   ;OXMWWd..lXWWMK, ;KWMMO'     :XWMx.;,    
    ',cNNkkNWWMXo.  lNWXc.     ,0WO'   :0XMMMo   lXWMX; .kWMWk.     .kWNl ..    
    ..'OMWNNK0d'   .kWXo.       lNX:   .'oNWWc    :ONN:  ;0KNd.      cx:.       
     .lKKk:'''.    c0o,.        .dk.     .;cd;     .dK;   ..:;.     .c:,.       

                                                             
      """)
 
