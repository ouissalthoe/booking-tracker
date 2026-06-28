import time
import datetime
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from telegram import Bot


# ------------------ YOUR INFO ------------------
BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"


# ------------------ CHROME ------------------
options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)


# ------------------ DATES ------------------
today = datetime.date.today()
checkin = today + datetime.timedelta(days=1)
checkout = today + datetime.timedelta(days=2)


# ------------------ URL ------------------
url = f"https://www.booking.com/searchresults.html?ss=voco+monaco+dubai&checkin_year={checkin.year}&checkin_month={checkin.month}&checkin_monthday={checkin.day}&checkout_year={checkout.year}&checkout_month={checkout.month}&checkout_monthday={checkout.day}&group_adults=2&no_rooms=1"

driver.get(url)
time.sleep(8)


# ------------------ OPEN HOTEL ------------------
hotel = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-testid='title-link']"))
)
hotel.click()

time.sleep(5)


# ------------------ GET ROOMS ------------------
rooms = driver.find_elements(By.CSS_SELECTOR, "[data-testid='room-card']")


message = f"📅 {checkin} - {checkout} BOOKING.COM\n\n"
message += "Room category | Room Only | Breakfast | Dinner\n\n"


def extract_prices(text):
    return re.findall(r"\d+", text)


for r in rooms:
    try:
        name = r.find_element(By.CSS_SELECTOR, "h2").text

        text = r.text
        prices = extract_prices(text)

        # we expect 3 prices per room (may vary)
        if len(prices) >= 3:
            room_only = float(prices[0])
            breakfast = float(prices[1])
            dinner = float(prices[2])

            # apply -10%
            ro = round(room_only * 0.9, 1)
            bf = round(breakfast * 0.9, 1)
            dn = round(dinner * 0.9, 1)

            message += f"{name}\n"
            message += f"{room_only} → {ro} | {breakfast} → {bf} | {dinner} → {dn}\n\n"

    except:
        continue


driver.quit()


# ------------------ TELEGRAM ------------------
bot = Bot(token=BOT_TOKEN)
bot.send_message(chat_id=CHAT_ID, text=message)

print("DONE")
