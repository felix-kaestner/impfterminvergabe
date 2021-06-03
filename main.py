from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from time import sleep

timeout = 30  # seconds

username = "Axxx-xxxxx"
password = "12345"

partner_username = None
partner_password = None

path = "C:\chromedriver.exe"

registration_url = "https://sachsen.impfterminvergabe.de/civ.public/start.html?oe=00.00.IM&mode=cc&cc_key=IOAktion"

driver = webdriver.Chrome(path)
driver.get(registration_url)

locations = {
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


def get_element(locator):
    return WebDriverWait(driver, timeout).until(expected_conditions.presence_of_element_located(locator))


def navigate_next():
    driver.find_element_by_id("WorkflowButton-4212").click()


def navigate_back():
    driver.find_element_by_id("WorkflowButton-4255").click()


def page_1():
    username_input = get_element((By.ID, "gwt-uid-3"))
    password_input = get_element((By.ID, "gwt-uid-5"))

    username_input.send_keys(username)
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

    username_input = get_element((By.ID, "gwt-uid-55"))
    password_input = get_element((By.ID, "gwt-uid-57"))

    username_input.send_keys(partner_username)
    password_input.send_keys(partner_password)


def open_location_dropdown():
    select = get_element((By.CSS_SELECTOR, ".select2-selection"))
    driver.execute_script("window.scrollTo(0, 600);")

    action = ActionChains(driver)
    action.move_to_element_with_offset(select, 5, 5)
    action.click()
    action.perform()


def query_location(value, name):
    open_location_dropdown()

    option = get_element((By.CSS_SELECTOR, f"li[id$=\"{value}\"]"))
    driver.execute_script("arguments[0].scrollIntoView(true);", option)
    option.click()

    navigate_next()

    # noinspection PyBroadException
    try:
        get_element((By.XPATH, '//*[text() = "Aufgrund der aktuellen Auslastung der Impfzentren und der verfügbaren '
                               'Impfstoffmenge können wir Ihnen leider keinen Termin anbieten. Bitte versuchen Sie es '
                               'in ein paar Tagen erneut."]'))
        print(f"    No appointments at: {name}")
        navigate_back()
    except:
        print(f"    Open appointments at: {name}")
        sleep(60 * 24)


def main():
    page_1()
    page_2()
    page_3()


if __name__ == '__main__':
    main()
