import time
import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from telegram import Bot


# 🔴 PUT YOUR INFO HERE (IMPORTANT)
BOT_TOKEN = "8868846049:AAE6syp1iH8NXv2y0ehsSBiVJcdLUAmHy3g"
CHAT_ID = "8419437999"


# ----------------- CHROME SETUP -----------------
options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

wait = WebDriverWait(driver, 20)


# ----------------- DATES -----------------
today = datetime.date.today()
checkin = today + datetime.timedelta(days=1)
checkout = today + datetime.timedelta(days=2)


# ----------------- URL -----------------
url = f"https://www.booking.com/searchresults.html?ss=voco+monaco+dubai&checkin_year={checkin.year}&checkin_month={checkin.month}&checkin_monthday={checkin.day}&checkout_year={checkout.year}&checkout_month={checkout.month}&checkout_monthday={checkout.day}&group_adults=2&no_rooms=1"

driver.get(url)
time.sleep(8)


# ----------------- OPEN HOTEL -----------------
try:
    hotel = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-testid='title-link']"))
    )
    hotel.click()
except:
    driver.quit()
    raise Exception("Hotel not found")


time.sleep(5)


# ----------------- GET ROOMS -----------------
rooms = driver.find_elements(By.CSS_SELECTOR, "[data-testid='room-card']")

message = "📅 Hotel Prices\n\n"

for r in rooms:
    try:
        name = r.find_element(By.CSS_SELECTOR, "h2").text
        price = r.text

        message += f"{name}\n{price}\n\n"
    except:
        continue


driver.quit()


# ----------------- SEND TO TELEGRAM -----------------
bot = Bot(token=BOT_TOKEN)
bot.send_message(chat_id=CHAT_ID, text=message)

print("DONE")
