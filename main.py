import datetime
import selenium
import time
import calendar
import threading
import sys
import random
import datetime
import json
from tkinter import *
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from datetime import timedelta
class UI:
    def __init__(self):
        ##Constants
        self.link = "https://sso.wis.ntu.edu.sg/webexe88/owa/sso_login1.asp?t=1&p2=https://wis.ntu.edu.sg/pls/webexe88/srce_smain_s.Notice_O&pg="
        self.BADMINTON = "Badminton@North Hill"
        self.SQUASH = "Squash@NTU Campus Clubhouse"
        self.TENNIS = "Tennis Court@SRC"
        self.chosen_time_list = tuple([dt.strftime('%H:%M') for dt in self.datetime_range(datetime.datetime(2022,1,1,9), datetime.datetime(2022,1,1,22),timedelta(minutes=60))])
        self.chosen_time_dict = {}
        for i in range(len(self.chosen_time_list)):
            self.chosen_time_dict[self.chosen_time_list[i]] = i+1
        print(self.chosen_time_dict)
        print(self.chosen_time_list)
        self.location_id_dict = {
            self.BADMINTON:0,
            self.SQUASH:2,
            self.TENNIS:5
        }
        self.court_identifier_dict = {
            self.BADMINTON:"1BB2BB",
            self.SQUASH:"1QS2QS",
            self.TENNIS:"1TS2TS"
        }
        self.shared_thread_data = ""
        self.last_shared_thread_data = ""
        self.threadlist = []
        ##UI top
        self.top = Tk()
        self.top.title("NTU Court Booking")
        # self.top.mainloop()
        ##UI Init
        self.chosen_loc = StringVar(self.top)
        self.chosen_loc.set(self.BADMINTON)
        Label(self.top, text="IMPORTANT: MAKE SURE YOU ENTER YOUR PASSWORD CORRECTLY\nOR RISK GETTING YOUR ACCOUNT LOCKED\n").grid(row=0, columnspan=3)
        Label(self.top, text="Network ID: ").grid(row=1)
        self.network_ID_entry = Entry(self.top)
        self.network_ID_entry.grid(row=1, column=1)
        Label(self.top, text="Password: ").grid(row=2)
        self.password_entry = Entry(self.top)
        self.password_entry.grid(row=2, column=1)
        self.loc_drop_down = OptionMenu(self.top, self.chosen_loc, self.BADMINTON, self.SQUASH, self.TENNIS)
        self.loc_drop_down.grid(row=3)
        self.chosen_time = StringVar(self.top)
        self.chosen_time.set(self.chosen_time_list[0])
        self.time_drop_down = OptionMenu(self.top, self.chosen_time, *self.chosen_time_list)
        self.time_drop_down.grid(row=3, column=2)
        self.submit_button = Button(self.top, text="SUBMIT", command=threading.Thread(target=self.submit_callback).start)
        self.submit_button.grid(row=4)
        # self.new_booking_button = Button(self.top, text="NEW BOOKING", command=threading.Thread(target=self.new_booking_button_callback).start)
        # self.new_booking_button.grid(row=3, column=2)
        self.text_output = Text(self.top, height=5)
        self.text_output.grid(row=5, columnspan=3)
        self.top.after(1000, self.refresh_data)
        self.top.mainloop()

    def refresh_data(self):
        # print(f"shared data: {self.shared_thread_data}")
        if self.last_shared_thread_data == "Booking succeeded :D":
            self.text_output.insert(END,"Booking succeeded :D")
            return
        if self.shared_thread_data != self.last_shared_thread_data:
            self.text_output.insert(END,self.shared_thread_data+"\n")
            self.last_shared_thread_data = self.shared_thread_data
        self.top.after(1000, self.refresh_data)

    def datetime_range(self, start, end, delta):
        current = start
        while current < end:
            yield current
            current += delta

    def submit_callback(self):
        try:
            booking_date = datetime.datetime.strftime(datetime.date.today() + datetime.timedelta(days=8), '%d/%m/%y')
            self.shared_thread_data = f"Booking for {booking_date}"
            username = self.network_ID_entry.get()
            password = self.password_entry.get()
            chosen_time_slot = self.chosen_time_dict[self.chosen_time.get()]
            for court_number in range(6):
                print(self.court_identifier_dict[self.chosen_loc.get()])
                print(self.location_id_dict[self.chosen_loc.get()])
                t = threading.Thread(target=self.automation,args=tuple([[username,password],booking_date,court_number+1,chosen_time_slot, self.court_identifier_dict[self.chosen_loc.get()], self.location_id_dict[self.chosen_loc.get()]]))
                t.start()
                self.threadlist.append(t)

            for thread in self.threadlist:
                thread.join()
        except:
            self.shared_thread_data = "Please open another instance to book!"

    def automation(self, account, booking_date, court_number, slot, court_identifier, loc_id):
        username,password = account
        chrome_options = Options()
        settings = {
           "recentDestinations": [{
                "id": "Save as PDF",
                "origin": "local",
                "account": "",
            }],
            "selectedDestinationId": "Save as PDF",
            "version": 2
        }
        prefs = {'printing.print_preview_sticky_settings.appState': json.dumps(settings)}
        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.add_argument('--kiosk-printing')
        chrome_options.add_argument("--headless")
        browser = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)
        browser.implicitly_wait(8)
        browser.set_window_size(1200, 600)
        browser.get(self.link)

        now = datetime.datetime.now().time()
        login_time = now.replace(hour=23, minute=58, second=0, microsecond=0)

        self.shared_thread_data = "Waiting to login at " + str(login_time)
        while datetime.datetime.now().time() < login_time:
            pass

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
            WebDriverWait(browser, 3).until(EC.alert_is_present())
            alert = browser.switch_to.alert
            alert.accept()
            self.shared_thread_data = "ERROR: Wrong Network ID or Password! Restart this window to book again."
            browser.close()
            return
        except TimeoutException:
            print("no alert")
        facilities_view = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.NAME, "p_info")))
        radio_button = browser.find_elements_by_name("p_info")[loc_id]
        self.shared_thread_data = "Logged in"
        # radio_button = browser.find_elements_by_name("p_info")[2]
        booking_date = datetime.datetime.strptime(booking_date, '%d/%m/%y')

        run_date = datetime.datetime.now().date() + datetime.timedelta(days=1)
        run_date = datetime.datetime.combine(run_date, datetime.time.min)
        print(run_date)
        while datetime.datetime.now() < run_date:
            pass
        radio_button.click()
        self.shared_thread_data = "Searching for available courts..."
        for _ in range(6):
            try:
                court_data = f"{court_identifier}{self.int_formatting(court_number)}{self.int_formatting(booking_date.day)}-{calendar.month_abbr[booking_date.month]}-{str(booking_date.year)}{str(slot)}"
                print(court_data)
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
            self.shared_thread_data = "Booking unsuccessful :("
        if browser.current_url == "https://wis.ntu.edu.sg/pls/webexe88/srce_sub1.srceb$sel33":
            self.shared_thread_data = "Booking succeeded :D"
        browser.close()

    def print_for_acc(self, string,email):
        print(string + " - " + email)
        return string + " - " + email

    def int_formatting(self, inpt):
        if (int(inpt) < 10):
            return "0"+str(inpt)
        return str(inpt)

    # def new_booking_button_callback(self):
    #     threading.Thread(target=UI).start()




if __name__ == "__main__":
    ui = UI()
