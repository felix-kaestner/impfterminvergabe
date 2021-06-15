from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException        
import sys
import os
import pathlib
import argparse
from time import sleep
import time
from pprint import pprint
import _thread
from pprint import pprint
import easygui
import os.path
from simplebeep import beep

parser = argparse.ArgumentParser(description='Auto-check the Impfterminvergabe-Website of Saxony.')

parser.add_argument('--username', type=str, help='Username')
parser.add_argument('--password', type=str, help='Password')
parser.add_argument('--impfzentrum', type=str, nargs="+", action="append", help='Impfzentrum Name/ID')
parser.add_argument('--partner_username', type=str, nargs='?', help='Partner username')
parser.add_argument('--partner_password', type=str, nargs='?', help='Partner password')

args = parser.parse_args()

timeout = 60  # seconds
short_timeout = 40  # seconds
kill_threads = False

username = args.username
if username is None:
    username = ""
    while username == "":
        username = easygui.enterbox("Please enter your username")
password = args.password
if password is None:
    password = ""
    while password == "":
        password = easygui.passwordbox("Please enter your password")

partner_username = args.partner_username
if partner_username is None and os.name == "nt":
    partner_username = easygui.enterbox("Please enter your partner username (can be empty)")
    if partner_username == "":
        partner_username = None
partner_password = args.partner_password
if partner_password is None and os.name == "nt":
    partner_password = easygui.enterbox("Please enter your partner password (can be empty)")
    if partner_password == "":
        partner_password = None

basepath = pathlib.Path(__file__).parent.absolute()
path = None

if os.name == 'nt':
    path = str(basepath) + "/chromedriver.exe"
    if not os.path.isfile(path) :
        wd = sys._MEIPASS
        path = os.path.join(wd, "chromedriver.exe")
elif os.name == "posix":
    path = str(basepath) + "/chromedriver"
else:
    print("Unknown operating system " + os.name)
    sys.exit(1)

registration_url = "https://sachsen.impfterminvergabe.de/civ.public/start.html?oe=00.00.IM&mode=cc&cc_key=IOAktion"

all_locations = {
    "BG01": "Stadthalle Belgern, Mühlberger Str. 37, 04874 Belgern-Schildau",
    "BN01": "ehem. Aldi Markt Borna, Oststraße 3a, 04552 Borna",
    "BZ01": "Sporthalle am Flughafen, Macherstraße 146, 01917 Kamenz",
    "CN01": "Richard-Hartmann-Halle, Fabrikstraße 9, 09111 Chemnitz",
    "DD01": "Messe Dresden, Messering 6, 01067 Dresden",
    "EC01": "Spektrum Treuen/Eich (ehem. Baumarkt), Rebesgrüner Str. 9, 08223 Treuen OT Eich",
    "EZ01": "Festhalle Annaberg-Buchholz, Ernst-Roch-Straße 4, 09456 Annaberg-Buchholz",
    "GR01": "TIZ Grimma, Muldentalhalle, Südstraße 80, 04668 Grimma",
    "LB01": "Messehalle Löbau, Görlitzer Str. 2, 02708 Löbau",
    "LZ01": "Messe Leipzig, Messe-Allee 1, 04356 Leipzig",
    "MW01": "Mittweida über Simmel-Markt (ehem. EKZ), Schillerstraße 1, 09648 Mittweida",
    "PN01": "Aldi Pirna Jessen, Radeberger Str. 1h, 01796 Pirna",
    "RI01": "Sachsen-Arena Riesa, Am Sportzentrum 5, 01589 Riesa",
    "ZW01": "Stadthalle Zwickau, Bergmannsstraße 1, 08056 Zwickau"
}

locations = {}
if args.impfzentrum is not None:
    for location_id in all_locations:
        location_name = all_locations[location_id]
        for this_impfzentrum in args.impfzentrum[0]:
            if this_impfzentrum in location_id or this_impfzentrum in location_name:
                locations[location_id] = location_name
else:
    if os.name == 'nt':
        chosen_location_name = None
        while chosen_location_name is None or chosen_location_name == "":
            chosen_location_name = easygui.enterbox("Please enter your location name")
        if chosen_location_name is not None:
            for location_id in all_locations:
                location_name = all_locations[location_id]
                if chosen_location_name in location_id or chosen_location_name in location_name:
                    locations[location_id] = location_name
    else:
        locations = all_locations

driver = webdriver.Chrome(path)
driver.get(registration_url)

def countdown (t):
    global kill_threads
    while t:
        if kill_threads:
            kill_threads = False
            _thread.exit()
        mins, secs = divmod(t, 60)
        timeformat = 'This operation may take time. ETA: {:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        t -= 1

def check_exists_by_id(item_id):
    html = driver.page_source
    if item_id in html:
        return True
    return False

def get_element_short_timeout(locator):
    global kill_threads
    countdown_thread = _thread.start_new_thread(countdown,(short_timeout,))
    item = WebDriverWait(driver, short_timeout).until(expected_conditions.presence_of_element_located(locator))
    kill_threads = True
    return item

def get_element(locator):
    global kill_threads
    countdown_thread = _thread.start_new_thread(countdown,(timeout,))
    item = WebDriverWait(driver, short_timeout).until(expected_conditions.presence_of_element_located(locator))
    kill_threads = True
    return item


def navigate_next():
    driver.find_element_by_id("WorkflowButton-4212").click()


def navigate_back():
    driver.find_element_by_id("WorkflowButton-4255").click()


def page_1():
    username_input = get_element((By.ID, "gwt-uid-3"))
    password_input = get_element((By.ID, "gwt-uid-5"))

    username_input.send_keys(username)
    sleep(2)
    password_input.send_keys(password)

    navigate_next()


def page_2():
    option_label = get_element((By.CSS_SELECTOR, "#gwt-uid-9 + label"))
    option_label.click()

    navigate_next()


def page_3():
    if partner_username is not None and partner_password is not None and username != partner_username and password != partner_password:
        fill_partner()

    while True:
        for value, name in locations.items():
            print(f"Try location: {name}")
            query_location(value, name)


def fill_partner():
    option_label = get_element((By.CSS_SELECTOR, "#gwt-uid-44 + label"))
    option_label.click()

    try:
        username_input = get_element((By.ID, "gwt-uid-55"))
        password_input = get_element((By.ID, "gwt-uid-57"))

        username_input.send_keys(partner_username)
        password_input.send_keys(partner_password)
    except:
        print(f"ERROR")


def open_location_dropdown():
    select = get_element((By.CSS_SELECTOR, ".select2-selection"))
    driver.execute_script("window.scrollTo(0, 600);")

    action = ActionChains(driver)
    action.move_to_element_with_offset(select, 5, 5)
    action.click()
    action.perform()

def open_appointments(name):
    print(f"    Open appointments at: {name}")
    driver.switch_to.window(driver.current_window_handle)
    for i in range(0, 5):
        beep(1, 1)
        sleep(1)
    sleep(3600)
    sys.exit(0)

def query_location(value, name):
    global driver
    open_location_dropdown()

    option = get_element((By.CSS_SELECTOR, f"li[id$=\"{value}\"]"))
    driver.execute_script("arguments[0].scrollIntoView(true);", option)
    option.click()

    navigate_next()

    # noinspection PyBroadException
    try:
        get_element_short_timeout((By.XPATH, '//*[text() = "Aufgrund der aktuellen Auslastung der Impfzentren und der verfügbaren '
                               'Impfstoffmenge können wir Ihnen leider keinen Termin anbieten. Bitte versuchen Sie es '
                               'in ein paar Tagen erneut."]'))
        print(f"    No appointments at: {name}")
        navigate_back()
    except:
        try:
            print(f"Checking for server errors. This may take up to " + timeout + " seconds")

            if get_element_short_timeout((By.XPATH, '//*[text() = "Internal Server Error - Write"]')):
                print(f"    ERROR. Restarting browser window")
                driver.quit()
                driver.close()
                driver = None
                driver = webdriver.Chrome(path)
                driver.get(registration_url)
                main
        except:
            open_appointments(name)

def main():
    page_1()
    page_2()
    page_3()

if __name__ == '__main__':
    main()
