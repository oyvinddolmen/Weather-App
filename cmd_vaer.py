from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH = "C:/Program Files (x86)/chromedriver.exe"


def get_weather():

    try:
        url = "https://www.yr.no/nb/i-nærheten/1-2893963/Norge/Viken/Kongsberg/Fjerdingstadgrenda"
        driver = webdriver.Chrome(PATH)
        driver.get(url)
        driver.implicitly_wait(15)

        # finner temperatur, venter på at nettsiden laster inn
        def get_temp_raw():
            temp_now_raw = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR,
                     "span[class='temperature observations-card-content__observed-value temperature--warm']"))
            ).get_attribute("innerHTML").strip()
            return temp_now_raw

        # finner temperaturen nå
        def get_number_in_temp_now(temp_now):
            temp_now_digit = ""
            # loop igjennom temperaturstringen, idgidigt() returnerer bare int og legger det i en variabel
            for char in temp_now:
                if char.isdigit() or char == ",":
                    temp_now_digit += char

            # endrer fra komma til punktum
            new_temp_now_digit = ""
            for char in temp_now_digit:
                # er det tall, lar vi den gå
                if char.isdigit():
                    new_temp_now_digit += char
                # hvis komma, gjør om til punktum
                if char == ",":
                    char = "."
                    new_temp_now_digit += char

            return new_temp_now_digit

        # går inn på værvarsel nav
        def change_page():
            vaervasel_nav = driver.find_element_by_css_selector(
                "a[class='location-header__menu-link']"
            )
            vaervasel_nav.click()

        # finner riktig symbol
        def check_weather_type():
            symbol_img = driver.find_element_by_class_name("symbol__img")
            current_weather_symbol = symbol_img.get_attribute("alt")
            return current_weather_symbol

        temperature = get_number_in_temp_now(get_temp_raw())

        change_page()
        weather_type = check_weather_type()
        print("Det er " + temperature + " C° og " + weather_type)

        # lukker chromedriver
        driver.quit()


    except Exception as e:
        if "in path" in str(e):
            print("Noe er galt med PATH")
        else:
            print("Noe gikk galt...")
            raise
        driver.quit()


get_weather()

