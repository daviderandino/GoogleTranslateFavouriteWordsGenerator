import undetected_chromedriver as uc
import time
from selenium.webdriver.common.by import By
import os
import pyautogui
import csv
import pyperclip

words = {}
chiavi = list()

def add_chrome_options():

    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--profile-directory=Default")
    chrome_options.add_argument("--disable-plugins-discovery")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("user_agent=DN")

    driver = uc.Chrome(options=chrome_options)
    driver.delete_all_cookies()
    return driver

def google_login():
    driver = add_chrome_options()
    email = os.environ.get('EMAIL') # environment variable
    password = os.environ.get('PASSWORD') # environment variable
    driver.get('https://accounts.google.com/servicelogin')
    time.sleep(3)
    search_form = driver.find_element(By.ID,"identifierId")
    search_form.send_keys(email)
    nextButton = driver.find_elements(By.XPATH,'//*[@id ="identifierNext"]') 
    nextButton[0].click()
    time.sleep(3)
    search_form = driver.find_element(By.NAME,"Passwd")
    search_form.send_keys(password)
    time.sleep(3)
    nextButton = driver.find_elements(By.XPATH,'//*[@id ="passwordNext"]')
    nextButton[0].click()
    time.sleep(5)
    driver.get('https://translate.google.it/saved?hl=it')
    export_google_sheet(driver)
    
def export_google_sheet(driver):
    body = driver.find_element(By.TAG_NAME,"body")
    original = body.text
    newer = original
    while original == newer:
        driver.get("https://translate.google.it/saved?hl=itm")
        body = driver.find_element(By.TAG_NAME,"body")
        newer = body.text
        time.sleep(5)
    print("modifica rilevata: bisogna modificare il DB")
    time.sleep(5)
    export_button = driver.find_element(By.XPATH,f"//*[@jsname='{'mAozAc'}']")
    export_button.click()
    time.sleep(20)
    # Simulate Ctrl + A (select all)
    pyautogui.hotkey('ctrl', 'a')

    # Simulate Ctrl + C (copy)
    pyautogui.hotkey('ctrl', 'c')

    time.sleep(5)
    
    confirm_button = driver.find_element(By.ID,"confirmActionButton")
    confirm_button.click()
    time.sleep(3)
    fill_csv_file(driver)
    

def fill_csv_file(driver):
    file_path = "words.csv"  

    with open(file_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        clipboard_text = pyperclip.paste()
        csv_writer.writerow([clipboard_text])
    
    time.sleep(5)
    pyautogui.hotkey('ctrl', 'w')
    time.sleep(3)
    export_google_sheet(driver)  

google_login()
