import os
import time
import datetime
import random
import re
import requests

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

PROXIES = [
    os.getenv("PROXY_1"),
    os.getenv("PROXY_2"),
    os.getenv("PROXY_3"),
]


def send_telegram(message):
    print("DEBUG TELEGRAM:", message)

    if not message or not message.strip():
        return

    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": message},
            timeout=20
        )
    except Exception as e:
        print("Telegram error:", e)


def get_proxy():
    proxies = [p for p in PROXIES if p]
    return random.choice(proxies) if proxies else None


def create_driver():
    options = uc.ChromeOptions()

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")

    print("DEBUG: starting Chrome...")

    driver = uc.Chrome(options=options, version_main=149)

    print("DEBUG: Chrome started successfully")

    return driver


def scrape():
    driver = None

    try:
        driver = create_driver()
        wait = WebDriverWait(driver, 25)

        today = datetime.date.today()
        checkin = today + datetime.timedelta(days=1)
        checkout = today + datetime.timedelta(days=2)

        url = (
            "https://www.booking.com/searchresults.html"
            f"?ss=voco+monaco+dubai"
        )

        print("DEBUG: opening URL")
        driver.get(url)

        time.sleep(8)

        print("DEBUG: page loaded")

        hotels = driver.find_elements(By.CSS_SELECTOR, "[data-testid='property-card']")

        print("DEBUG hotels:", len(hotels))

        if not hotels:
            raise Exception("No hotels found")

        hotels[0].click()

        time.sleep(8)

        rooms = driver.find_elements(By.CSS_SELECTOR, "[data-testid='room-card']")

        print("DEBUG rooms:", len(rooms))

        message = "BOT WORKING\n\n"
        send_telegram(message)

    except Exception as e:
        print("ERROR OCCURED:", str(e))
        send_telegram(f"❌ ERROR:\n{str(e)}")

    finally:
        if driver:
            driver.quit()


def main():
    print("BOT STARTED")
    scrape()


if __name__ == "__main__":
    main()
