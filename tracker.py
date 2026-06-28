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


def send_telegram(msg):
    print("DEBUG:", msg)

    if not msg:
        return

    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": msg},
            timeout=20
        )
    except:
        pass


def create_driver():
    options = uc.ChromeOptions()

    # IMPORTANT STEALTH FLAGS
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    # IMPORTANT: DO NOT FORCE HEADLESS FIRST (TEST MODE)
    options.add_argument("--headless=new")

    driver = uc.Chrome(options=options, version_main=149)

    return driver


def scrape():
    driver = None

    try:
        driver = create_driver()
        wait = WebDriverWait(driver, 30)

        today = datetime.date.today()
        checkin = today + datetime.timedelta(days=1)

        url = "https://www.booking.com/searchresults.html?ss=voco+monaco+dubai"

        print("OPENING PAGE")
        driver.get(url)

        time.sleep(10)

        # SAVE PAGE FOR DEBUG (VERY IMPORTANT)
        with open("debug.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

        print("PAGE TITLE:", driver.title)

        hotels = driver.find_elements(By.CSS_SELECTOR, "[data-testid='property-card']")

        print("HOTELS FOUND:", len(hotels))

        if len(hotels) == 0:
            raise Exception("No hotels found (blocked or CAPTCHA page)")

        hotels[0].click()

        time.sleep(8)

        rooms = driver.find_elements(By.CSS_SELECTOR, "[data-testid='room-card']")

        print("ROOMS:", len(rooms))

        send_telegram(f"OK WORKING ✅ Hotels: {len(hotels)} Rooms: {len(rooms)}")

    except Exception as e:
        send_telegram(f"❌ ERROR:\n{e}")
        print("ERROR:", e)

    finally:
        if driver:
            driver.quit()


def main():
    print("BOT STARTED")
    scrape()


if __name__ == "__main__":
    main()
