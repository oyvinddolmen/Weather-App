from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tkinter import *
from PIL import ImageTk, Image

root = Tk()
root.title("Værsjekker")
root.geometry("500x500")
root.iconbitmap("D:/OneDrive/PyCharm/egne_apllikasjoner/tkinter_selenium_yr/media/icon.ico")


PATH = "C:/Program Files (x86)/chromedriver.exe"


def get_weather():
    try:
        url = "https://www.yr.no/nb"
        driver = webdriver.Chrome(PATH)
        driver.get(url)
        driver.implicitly_wait(15)

        # Trykker på search feltet
        src_btn = driver.find_element_by_id("page-header__search-button")
        src_btn.click()

        # søker og trykker på Kongsberg
        src_field = driver.find_element_by_id("page-header__search-input")
        src_field.send_keys("Kongsberg")
        kbg_element = driver.find_element_by_class_name("search__suggestions")
        kbg_element.click()

        # finner temperatur, venter på at nettsiden laster inn
        def get_temp_raw():
            temp_now_raw = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "span[class='temperature min-max-temperature__max temperature--warm']"))
            ).get_attribute("innerHTML").strip()
            return temp_now_raw


        # finner temperaturen nå
        def check_for_number_in_temp_now(temp_now):
            temp_now_digit = ""
            # loop igjennom temperaturstringen, idgidigt() returnerer bare int og legger det i en variabel
            for char in temp_now:
                if char.isdigit():
                    temp_now_digit += char
                    print(temp_now_digit)
            return temp_now_digit


        def check_weather_type():
            symbol_img = driver.find_element_by_class_name("symbol__img")
            current_weather_symbol = symbol_img.get_attribute("alt")
            return current_weather_symbol

        temperature = check_for_number_in_temp_now(get_temp_raw())
        weather_type = check_weather_type()
        print("Det er " + temperature + "* og " + weather_type)


        # bestemmer rgb verdi som skal være bakgrunnsfarge
        def temperature_background():
            if int(temperature) < 0:
                if int(temperature) <= -19:
                    rgb = (0, 212, 255)
                    return rgb
                rgb = (255 - int((int(temperature) * int(temperature)) / 1.5), 255 + int(temperature) * 2, 255)
                return rgb

            elif int(temperature) >= 0:
                if int(temperature) > 20:
                    rgb = (255, 0, 0)
                    return rgb
                rgb = (255, 255 - int((int(temperature) * 12.5)), 255 - int((int(temperature) * 12.5)))
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
                img_symbol_name = "D:/OneDrive/PyCharm/egne_apllikasjoner/tkinter_selenium_yr/media/klarvær.jpg"
            elif weather_symbol == "lettskyet":
                img_symbol_name = "D:/OneDrive/PyCharm/egne_apllikasjoner/tkinter_selenium_yr/media/lettskyet.jpg"
            elif weather_symbol == "delvis_skyet":
                img_symbol_name = "D:/OneDrive/PyCharm/egne_apllikasjoner/tkinter_selenium_yr/media/delvis_skyet.jpg"
            elif weather_symbol == "skyet":
                img_symbol_name = "D:/OneDrive/PyCharm/egne_apllikasjoner/tkinter_selenium_yr/media/skyet.jpg"
            elif weather_symbol == "regn":
                img_symbol_name = "D:/OneDrive/PyCharm/egne_apllikasjoner/tkinter_selenium_yr/media/regn.jpg"
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
        my_label = Label(root, text="Det er " + temperature + "C* og " + weather_type + " i Kongsberg nå", font=("Arial", 20))
        my_label.grid(row=2, column=0, stick=E)
        show_weather_symbol()


    except Exception as e:
        if "in path" in str(e):
            print("Noe er galt med PATH")
        else:
            print("Noe gikk galt...")
            raise
        driver.quit()


get_weather()
mainloop()

