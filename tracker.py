import time
import datetime
import re
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException


# ------------------ TELEGRAM INFO ------------------
BOT_TOKEN = "YOUR_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"


def send_telegram(message):
    if not message or len(message.strip()) == 0:
        print("❌ EMPTY MESSAGE — NOT SENDING")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    try:
        r = requests.post(url, data=payload)
        print("TELEGRAM STATUS:", r.status_code)
        print("TELEGRAM RESPONSE:", r.text)
    except Exception as e:
        print("❌ TELEGRAM ERROR:", e)


# ------------------ CHROME ------------------
options = Options()
options.binary_location = "/usr/bin/chromium-browser"

options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

# 🔥 ANTI-BOT IMPROVEMENTS
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")

options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125 Safari/537.36"
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
time.sleep(10)


# ------------------ COOKIE ------------------
try:
    wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))).click()
except:
    pass


print("PAGE TITLE:", driver.title)


# ------------------ FIND HOTEL ------------------
try:
    hotels = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "[data-testid='property-card']")
        )
    )

    print("HOTELS FOUND:", len(hotels))

    if len(hotels) == 0:
        raise Exception("No hotels found (blocked)")

    hotel = hotels[0]

    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", hotel)
    time.sleep(2)

    try:
        hotel.click()
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].click();", hotel)

except Exception as e:
    driver.quit()
    send_telegram(f"❌ HOTEL PAGE ERROR:\n{e}")
    raise


# ------------------ ROOMS ------------------
time.sleep(10)

# 🔥 TRY MULTIPLE SELECTORS (VERY IMPORTANT)
rooms = driver.find_elements(By.CSS_SELECTOR, "[data-testid='room-card']")

if len(rooms) == 0:
    print("⚠️ room-card not found, trying fallback...")
    rooms = driver.find_elements(By.CSS_SELECTOR, "tr")


# 🔍 DEBUG SAVE PAGE
print("PAGE SOURCE LENGTH:", len(driver.page_source))

with open("page.html", "w", encoding="utf-8") as f:
    f.write(driver.page_source)


print("ROOMS FOUND:", len(rooms))

valid_rooms = 0

message = f"📅 {checkin} → {checkout}\n🏨 VOCO MONACO DUBAI\n\n"


def extract_numbers(text):
    return re.findall(r"\d+", text)


for r in rooms:
    try:
        name = r.text.split("\n")[0]
        text = r.text

        prices = extract_numbers(text)

        if len(prices) >= 3:
            valid_rooms += 1

            room_only = float(prices[0])
            breakfast = float(prices[1])
            dinner = float(prices[2])

            ro = round(room_only * 0.9, 1)
            bf = round(breakfast * 0.9, 1)
            dn = round(dinner * 0.9, 1)

            message += (
                f"{name}\n"
                f"RO: {room_only} → {ro}\n"
                f"BF: {breakfast} → {bf}\n"
                f"DN: {dinner} → {dn}\n\n"
            )

    except:
        continue

driver.quit()


# ------------------ SAFETY ------------------
print("VALID ROOMS:", valid_rooms)
print("MESSAGE LENGTH:", len(message))


if valid_rooms == 0:
    message = "⚠️ No valid rooms found.\nBooking is likely blocking GitHub IP."

if len(message.strip()) < 30:
    message = "⚠️ Scraper error: empty or invalid data."


print("FINAL MESSAGE:\n", message)


# ------------------ SEND ------------------
send_telegram(message)
