import time
import datetime
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException

from telegram import Bot


# ------------------ TELEGRAM INFO ------------------
BOT_TOKEN = "8868846049:AAE6syp1iH8NXv2y0ehsSBiVJcdLUAmHy3g"
CHAT_ID = 8419437999


# ------------------ CHROME ------------------
options = Options()
options.binary_location = "/usr/bin/chromium-browser"

options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
)

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 25)


# ------------------ DATES ------------------
today = datetime.date.today()
checkin = today + datetime.timedelta(days=1)
checkout = today + datetime.timedelta(days=2)


# ------------------ URL ------------------
url = (
    "https://www.booking.com/searchresults.html"
    f"?ss=voco+monaco+dubai"
    f"&checkin_year={checkin.year}&checkin_month={checkin.month}&checkin_monthday={checkin.day}"
    f"&checkout_year={checkout.year}&checkout_month={checkout.month}&checkout_monthday={checkout.day}"
    f"&group_adults=2&no_rooms=1"
)

driver.get(url)
time.sleep(25)


# ------------------ COOKIE ------------------
try:
    wait.until(
        EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
    ).click()
except:
    pass


# ------------------ HOTELS ------------------
hotels = wait.until(
    EC.presence_of_all_elements_located(
        (By.XPATH, "//div[contains(@data-testid,'property-card')]")
    )
)

print("HOTELS FOUND:", len(hotels))

if len(hotels) == 0:
    driver.quit()
    raise Exception("No hotels found")

hotel = hotels[0]

driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", hotel)
time.sleep(2)

try:
    hotel.click()
except ElementClickInterceptedException:
    driver.execute_script("arguments[0].click();", hotel)


# ------------------ ROOMS ------------------
time.sleep(8)

rooms = driver.find_elements(By.CSS_SELECTOR, "[data-testid='room-card']")
print("ROOMS FOUND:", len(rooms))

if len(rooms) == 0:
    driver.quit()
    raise Exception("❌ No rooms found → Booking blocked or selector broken")


# ------------------ MESSAGE BUILD ------------------
message = f"📅 {checkin} - {checkout} BOOKING.COM\n\n"
message += "Room category | Room Only | Breakfast | Dinner\n\n"


def extract_numbers(text):
    return re.findall(r"\d+", text)


for r in rooms:
    try:
        name = r.find_element(By.CSS_SELECTOR, "h2").text
        text = r.text

        prices = extract_numbers(text)

        if len(prices) >= 3:
            room_only = float(prices[0])
            breakfast = float(prices[1])
            dinner = float(prices[2])

            ro = round(room_only * 0.9, 1)
            bf = round(breakfast * 0.9, 1)
            dn = round(dinner * 0.9, 1)

            message += f"{name}\n"
            message += f"{room_only} → {ro} | {breakfast} → {bf} | {dinner} → {dn}\n\n"

    except:
        continue


driver.quit()


# ------------------ SAFETY CHECK ------------------
print("FINAL MESSAGE LENGTH:", len(message))

if len(message) < 150:
    message = "⚠️ No valid room data found or Booking blocked."


# ------------------ TELEGRAM ------------------
try:
    bot = Bot(token=8868846049:AAE6syp1iH8NXv2y0ehsSBiVJcdLUAmHy3g)
    bot.send_message(chat_id=8419437999, text=message)
    print("TELEGRAM SENT SUCCESSFULLY")
except Exception as e:
    print("TELEGRAM ERROR:", e)
    raise
