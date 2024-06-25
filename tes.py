from selenium import webdriver
from selenium.webdriver.common.by import By
from base64 import b64decode
import json
import datetime
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import requests


#add detach
options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
driver.get("file:///C:/Users/anggn/Downloads/siakbot/siakbot/siakcourseplan.html")
driver.execute_script("arguments[0].checked = 'checked';", driver.find_element(By.XPATH, "//input[@value='709120-4']"))

