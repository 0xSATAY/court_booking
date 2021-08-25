#!/usr/bin/env python3

import selenium
import time
import calendar
import threading
import sys
import random
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

filename = "accounts.txt"
link = "https://sso.wis.ntu.edu.sg/webexe88/owa/sso_login1.asp?t=1&p2=https://wis.ntu.edu.sg/pls/webexe88/srce_smain_s.Notice_O&pg="
accounts = []

def read_accounts(filename):
    accounts = []
    with open(filename) as f:
        content = f.readlines()
        accounts = content
        for i in range(len(accounts)):
            accounts[i] = accounts[i][:-1]
    f.close()
    return accounts

def int_formatting(inpt):
    if (int(inpt) < 10):
        return "0"+str(inpt)
    return str(inpt)

def automation(account,booking_date):
    username,password = account.split(":")
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    browser = webdriver.Chrome("./chromedriver", options=chrome_options) #change this to your own chromedriver path "/Users/wangdian/chromedriver"
    browser.set_window_size(1200, 600)
    browser.get(link)

    now = datetime.now().time()
    login_time = now.replace(hour=23, minute=58, second=0, microsecond=0)

    print_for_acc("Waiting to login at " + str(login_time), username)
    # while datetime.now().time() < login_time:
    #     pass

    login_view = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "form-rounded")))
    username_field = browser.find_elements_by_class_name("form-rounded")[0]
    username_field.send_keys(username)
    ok_button = browser.find_elements_by_class_name("form-rounded")[2]
    ok_button.click()
    password_field = browser.find_elements_by_class_name("form-rounded")[0]
    password_field.send_keys(password)
    ok_button = browser.find_elements_by_class_name("form-rounded")[1]
    ok_button.click()

    facilities_view = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.NAME, "p_info")))
    radio_button = browser.find_elements_by_name("p_info")[16]
    radio_button.click()
    booking_date = datetime.strptime(booking_date, '%d/%m/%y').replace(second=2)
    while datetime.now() < booking_date:
        pass
    try:
        # court_data = "1BB2BB"+int_formatting(i)+int_formatting(booking_date.day)+"-"+calendar.month_abbr[booking_date.month]+"-"+str(booking_date.year)+"12"
        for i in [1,2,3,4,5,6]:
            court_data = f"1BK2BK{int_formatting(i)}{int_formatting(booking_date.day)}-{calendar.month_abbr[booking_date.month]}-{str(booking_date.year)}6"
            xpath = f"//input[@value='{court_data}']"
            court_radio_button = browser.find_element_by_xpath(xpath)
            court_radio_button.click()
            print(court_data)

    except:
        pass
    confirmation_view = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.NAME, "bOption")))
    confirm_button = browser.find_elements_by_name("bOption")[0]
    confirm_button.click()

    while True:
        pass

def print_for_acc(string,email):
    print(string + " - " + email)


def main():
    global link
    global size
    global accounts
    args = sys.argv
    try:
        filename = args[1]
        accounts = read_accounts(args[1])
        booking_date = args[2]
        threadlist = []

        for i in range(len(accounts)):
            t = threading.Thread(target=automation,args=tuple([accounts[i],booking_date]))
            t.start()
            threadlist.append(t)

        for thread in threadlist:
            thread.join()
    except:
        print("ERROR: Please fill in valid parameters")
        print("USAGE: python3 badminton_booking.py <account details file> <date (format:dd/mm/yy)>")
        print("On bash: ./badminton_booking.py <account details file> <date (format:dd/mm/yy)>")
        return

if __name__ == "__main__":
    main()
