import time
import datetime
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import telegram

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Setup browser
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

# Dates (next 7 days)
today = datetime.date.today()
checkin = today + datetime.timedelta(days=1)
checkout = today + datetime.timedelta(days=2)

url = f"https://www.booking.com/searchresults.html?ss=voco+monaco+dubai&checkin_year={checkin.year}&checkin_month={checkin.month}&checkin_monthday={checkin.day}&checkout_year={checkout.year}&checkout_month={checkout.month}&checkout_monthday={checkout.day}&group_adults=2&no_rooms=1&group_children=0"

driver.get(url)
time.sleep(10)

# Open hotel page
driver.find_element(By.CSS_SELECTOR, "a[data-testid='title-link']").click()
time.sleep(10)

# Extract room data
rooms = driver.find_elements(By.CSS_SELECTOR, "[data-testid='room-card']")

message = f"📅 Voco Monaco Dubai Rates (2 Adults)\n"
message += f"{checkin} → {checkout}\n\n"

for room in rooms:
    try:
        name = room.find_element(By.CSS_SELECTOR, "h2").text
        prices = room.find_elements(By.CSS_SELECTOR, "[data-testid='price-and-discounted-price']")

        message += f"🏨 {name}\n"

        for p in prices[:3]:
            price_text = p.text.replace(",", "")
            price = float(''.join(filter(str.isdigit, price_text)))

            discounted = round(price * 0.9, 1)

            message += f"{price} → {discounted}\n"

        message += "\n"

    except:
        continue

driver.quit()

# Send to Telegram
bot = telegram.Bot(token=BOT_TOKEN)
bot.send_message(chat_id=CHAT_ID, text=message)
