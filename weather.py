from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tkinter import *
from PIL import ImageTk, Image

root = Tk()
root.title("Værsjekker")
root.geometry("500x500")
root.iconbitmap("D:/OneDrive/programmering/egne_apllikasjoner_python/tkinter_selenium_yr/media/icon.ico")

PATH = "C:/Program Files (x86)/chromedriver.exe"


def get_weather():
    try:
        url = "https://www.yr.no/nb/i-nærheten/1-58196/Norge/Viken/Kongsberg/Kongsberg"
        driver = webdriver.Chrome(PATH)
        driver.get(url)
        driver.implicitly_wait(10)

        # finner temperatur, venter på at nettsiden laster inn
        def get_temp_raw():

            # NB !!!!! "cold" må byttes ut med "warm" hvis plussgrader
            temp_now_raw = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR,
                        "span[class='temperature observations-card-content__observed-value temperature--cold']"))
            ).get_attribute("innerHTML").strip()

            print(temp_now_raw)
            return temp_now_raw

        # finner temperaturen nå
        def get_number_in_temp_now(temp_now):
            temp_now_digit = ""
            # loop igjennom temperaturstringen, idgidigt() returnerer bare int og legger det i en variabel
            valid_characters = [",", "-", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
            for char in temp_now:
                if char in valid_characters:
                    temp_now_digit += char
                    print("Old temp now: " + temp_now_digit)

            # endrer fra komma til punktum
            new_temp_now_digit = ""
            for char in temp_now_digit:
                # er det tall eller "-", lar vi den gå
                if char.isdigit() or char == "-":
                    new_temp_now_digit += char
                # hvis komma, gjør om til punktum
                if char == ",":
                    char = "."
                    new_temp_now_digit += char

            # gjør at minusgrader også fungerer
            new_temp_now_digit = new_temp_now_digit[1:]
            string_len = len(new_temp_now_digit)
            new_temp_now_digit = new_temp_now_digit[:string_len - 1]
            print("New temp now: " + new_temp_now_digit)
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
        float_temp = float(temperature)
        temp = int(float_temp)
        print(temp)

        change_page()
        weather_type = check_weather_type()
        print("Det er " + temperature + "C° og " + weather_type)

        # bestemmer rgb verdi som skal være bakgrunnsfarge
        def temperature_background():
            # minusgrader
            if temp < 0:
                if temp <= -12:
                    rgb = (0, 212, 255)
                    return rgb
                rgb = (int(255 - ((temp * temp * 3) / 1.5)), int(255 + (temp * 2)), 255)
                return rgb

            # plussgrader
            elif temp >= 0:
                if temp > 20:
                    rgb = (255, 0, 0)
                    return rgb
                rgb = (255, int(255 - (temp * 12.5)), int(255 - (temp * 12.5)))
                print(rgb)
                return rgb

        # oversetter fra RGB til hex
        def rgb_to_hex(rgb_code):
            hex_color = "#%02x%02x%02x" % rgb_code
            print(hex_color)

            root.configure(background=hex_color)

        # funksjon som viser passende værsymbol
        def show_weather_symbol():
            weather_symbol = weather_type

            # sjekker hva alt er på bildene, og viser samme i tkinter
            if weather_symbol == "klarvær":
                img_symbol_name = "D:/OneDrive\programmering/egne_apllikasjoner_python/tkinter_selenium_yr\media/klarvær.jpg"
            elif weather_symbol == "lettskyet":
                img_symbol_name = "D:/OneDrive\programmering/egne_apllikasjoner_python/tkinter_selenium_yr\media/lettskyet.jpg"
            elif weather_symbol == "delvis_skyet":
                img_symbol_name = "D:/OneDrive\programmering/egne_apllikasjoner_python/tkinter_selenium_yr\media/delvis_skyet.jpg"
            elif weather_symbol == "skyet":
                img_symbol_name = "D:/OneDrive\programmering/egne_apllikasjoner_python/tkinter_selenium_yr\media/skyet.jpg"
            elif weather_symbol == "regn":
                img_symbol_name = "D:/OneDrive\programmering/egne_apllikasjoner_python/tkinter_selenium_yr\media/regn.jpg"
            else:
                img_symbol_name = "media/ukjent.jpg"

            current_weather_img = ImageTk.PhotoImage(Image.open(img_symbol_name))
            img_label = Label(root, image=current_weather_img)
            # når bildet brukes i en funksjon, må man lage en kobling slik at python ikke fjerner bildet-objektet
            img_label.image = current_weather_img
            img_label.grid(row=0, column=0)

        # TKINTER - skriver ut i tkinter:
        temperature_background()  # bestemmer rgb tuplen
        rgb_to_hex(temperature_background())  # sender med rgb til å øverføres til hex
        my_label = Label(root, text="Det er " + temperature + " C° og " + weather_type + " i Kongsberg nå",
                         font=("Arial", 20))
        my_label.grid(row=2, column=0, stick=E)
        show_weather_symbol()

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
mainloop()
