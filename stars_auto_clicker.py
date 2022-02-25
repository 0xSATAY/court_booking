from webdriver_manager.chrome import ChromeDriverManager
import selenium
import time
import calendar
import threading
import sys
import random
import datetime
import traceback
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert

accounts = []
link = "https://wish.wis.ntu.edu.sg/pls/webexe/ldap_login.login?w_url=https://wish.wis.ntu.edu.sg/pls/webexe/aus_stars_planner.main"

def read_accounts(filename):
    accounts = []
    with open(filename) as f:
        content = f.readlines()
        accounts = content
        for i in range(len(accounts)):
            accounts[i] = accounts[i].strip("\n")
    f.close()
    return accounts

def automation(account):
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    username,password = account.split(":")
    browser = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)
    browser.get(link)

    login_view = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "form-rounded")))
    username_field = browser.find_elements_by_class_name("form-rounded")[0]
    username_field.send_keys(username)
    ok_button = browser.find_elements_by_class_name("form-rounded")[2]
    ok_button.click()
    password_field = browser.find_elements_by_class_name("form-rounded")[0]
    password_field.send_keys(password)
    ok_button = browser.find_elements_by_class_name("form-rounded")[1]
    ok_button.click()
    try:
        while True:
            add_courses_button_exists = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH,"//input[@value='Add (Register) Selected Course(s)']")))
            add_courses_button = browser.find_element_by_xpath("//input[@value='Add (Register) Selected Course(s)']")
            add_courses_button.click()

            confirm_button_exists = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH,"//input[@value='Confirm to add course(s)']")))
            confirm_button = browser.find_element_by_xpath("//input[@value='Confirm to add course(s)']")
            confirm_button.click()

            back_to_timetable_button_exists = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH,"//input[@value='Back to Timetable']")))
            back_to_timetable_button = browser.find_element_by_xpath("//input[@value='Back to Timetable']")
            back_to_timetable_button.click()
    except:
        print(traceback.format_exc())
        print("Browser Restart")
        browser.close()
        automation(account)



def main():
    global link
    global accounts
    args = sys.argv
    accounts = read_accounts(args[1])
    threadlist = []
    for account_index in range(len(accounts)):
        t = threading.Thread(target=automation,args=tuple([accounts[account_index]]))
        t.start()
        threadlist.append(t)

    for thread in threadlist:
        thread.join()

if __name__ == "__main__":
    os.environ['WDM_LOG_LEVEL'] = '0'
    main()
