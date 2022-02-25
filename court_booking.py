#!/usr/bin/env python3

import selenium
import time
import calendar
import threading
import sys
import random
import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

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


def automation(account,booking_date,slot_list, court_number, slot):
    username,password = account.split(":")
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    browser = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)
    browser.implicitly_wait(8)
    browser.set_window_size(1200, 600)
    browser.get(link)

    now = datetime.datetime.now().time()
    login_time = now.replace(hour=23, minute=58, second=0, microsecond=0)

    print_for_acc("Waiting to login at " + str(login_time), username)
    # while datetime.datetime.now().time() < login_time:
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
    radio_button = browser.find_elements_by_name("p_info")[0]
    # radio_button = browser.find_elements_by_name("p_info")[2]
    booking_date = datetime.datetime.strptime(booking_date, '%d/%m/%y')

    run_date = datetime.datetime.now().date() + datetime.timedelta(days=1)
    run_date = datetime.datetime.combine(run_date, datetime.time.min)
    print(run_date)
    while datetime.datetime.now() < run_date:
        pass
    radio_button.click()
    for _ in range(6):
        try:
            # court_data = f"1BK2BK{int_formatting(i)}{int_formatting(booking_date.day)}-{calendar.month_abbr[booking_date.month]}-{str(booking_date.year)}9"
            court_data = "1BB2BB"+int_formatting(court_number)+int_formatting(booking_date.day)+"-"+calendar.month_abbr[booking_date.month]+"-"+str(booking_date.year)+str(slot)
            # court_data = "1QS2QS"+int_formatting(court_number)+int_formatting(booking_date.day)+"-"+calendar.month_abbr[booking_date.month]+"-"+str(booking_date.year)+"13"
            xpath = f"//input[@value='{court_data}']"
            court_radio_button = browser.find_element_by_xpath(xpath)
            court_radio_button.click()
            print(court_data)
            break

        except NoSuchElementException:
            browser.refresh()
            continue
    try:
        print("Enter confirmation view")
        confirmation_view = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.NAME, "bOption")))
        confirm_button = browser.find_elements_by_name("bOption")[0]
        confirm_button.click()
    except TimeoutException:
        print("Request timed out. Booking unsuccessful on this thread.")
def print_for_acc(string,email):
    print(string + " - " + email)


def main():
    global link
    global size
    global accounts
    args = sys.argv
    num_threads = 0
    try:
        accounts = read_accounts(args[1])
        booking_date = datetime.datetime.strftime(datetime.date.today() + datetime.timedelta(days=8), '%d/%m/%y')
        print(f"Booking for {booking_date}")
        threadlist = []

        for account_index in range(len(accounts)):
            for court_number in range(6):
                for slot_number in range(3):
                    t = threading.Thread(target=automation,args=tuple([accounts[account_index],booking_date,account_index+1,court_number+1,slot_number+12]))
                    t.start()
                    threadlist.append(t)

        for thread in threadlist:
            thread.join()
    except:
        print("ERROR: Please fill in valid parameters")
        print("USAGE: python3 badminton_booking.py <account details file>")
        print("On bash: ./badminton_booking.py <account details file>")
        return

if __name__ == "__main__":
    main()
