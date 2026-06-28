import time
import datetime
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from telegram import Bot


# -----------------------------
# CONFIG
# -----------------------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


# -----------------------------
# CHROME SETUP
# -----------------------------
options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

wait = WebDriverWait(driver, 20)


# -----------------------------
# DATES
# -----------------------------
today = datetime.date.today()
checkin = today + datetime.timedelta(days=1)
checkout = today + datetime.timedelta(days=2)


# -----------------------------
# BOOKING URL
# -----------------------------
url = (
    "https://www.booking.com/searchresults.html"
    f"?ss=voco+monaco+dubai"
    f"&checkin_year={checkin.year}&checkin_month={checkin.month}&checkin_monthday={checkin.day}"
    f"&checkout_year={checkout.year}&checkout_month={checkout.month}&checkout_monthday={checkout.day}"
    f"&group_adults=2&no_rooms=1&group_children=0"
)

driver.get(url)


# -----------------------------
# OPEN HOTEL PAGE
# -----------------------------
try:
    hotel_link = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-testid='title-link']"))
    )
    hotel_link.click()
except Exception as e:
    driver.quit()
    raise Exception("Could not open hotel page. Booking layout may have changed.") from e


# -----------------------------
# LOAD ROOMS
# -----------------------------
time.sleep(5)

rooms = driver.find_elements(By.CSS_SELECTOR, "[data-testid='room-card']")


# -----------------------------
# BUILD MESSAGE
# -----------------------------
message = f"📅 Voco Monaco Dubai Rates (2 Adults)\n"
message += f"{checkin} → {checkout}\n\n"


for room in rooms:
    try:
        name = room.find_element(By.CSS_SELECTOR, "h2").text.strip()

        price_elements = room.find_elements(
            By.CSS_SELECTOR,
            "[data-testid='price-and-discounted-price']"
        )

        message += f"🏨 {name}\n"

        for p in price_elements[:3]:
            text = p.text
            digits = "".join(filter(str.isdigit, text))

            if digits:
                price = int(digits)
                discounted = round(price * 0.9, 1)

                message += f"{price} → {discounted}\n"

        message += "\n"

    except:
        continue


driver.quit()


# -----------------------------
# SEND TO TELEGRAM
# -----------------------------
bot = Bot(token=BOT_TOKEN)
bot.send_message(chat_id=CHAT_ID, text=message)

print("Done: message sent")
