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


# ------------------ TELEGRAM (DO NOT PUT NUMBERS HERE) ------------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

PROXIES = [
    os.getenv("PROXY_1"),
    os.getenv("PROXY_2"),
    os.getenv("PROXY_3"),
]


def send_telegram(message):
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

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/125 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/124 Safari/537.36",
    ]

    options.add_argument(f"user-agent={random.choice(user_agents)}")

    proxy = get_proxy()
    if proxy:
        options.add_argument(f"--proxy-server={proxy}")

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")

    return uc.Chrome(options=options)


def scrape():
    driver = None

    try:
        driver = create_driver()
        wait = WebDriverWait(driver, 25)

        time.sleep(random.uniform(3, 7))

        today = datetime.date.today()
        checkin = today + datetime.timedelta(days=1)
        checkout = today + datetime.timedelta(days=2)

        url = (
            "https://www.booking.com/searchresults.html"
            f"?ss=voco+monaco+dubai"
            f"&checkin_year={checkin.year}&checkin_month={checkin.month}&checkin_monthday={checkin.day}"
            f"&checkout_year={checkout.year}&checkout_month={checkout.month}&checkout_monthday={checkout.day}"
            f"&group_adults=2&no_rooms=1"
        )

        driver.get(url)

        time.sleep(random.uniform(5, 10))

        try:
            wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))).click()
        except:
            pass

        hotels = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-testid='property-card']"))
        )

        hotel = hotels[0]
        hotel.click()

        time.sleep(random.uniform(6, 10))

        rooms = driver.find_elements(By.CSS_SELECTOR, "[data-testid='room-card']")
        if not rooms:
            rooms = driver.find_elements(By.CSS_SELECTOR, "tr")

        def extract_numbers(text):
            return re.findall(r"\d+", text)

        message = f"📅 {checkin} → {checkout}\n🏨 VOCO MONACO DUBAI\n\n"
        valid_rooms = 0

        for r in rooms:
            try:
                text = r.text
                prices = extract_numbers(text)

                if len(prices) >= 3:
                    valid_rooms += 1

                    ro = float(prices[0])
                    bf = float(prices[1])
                    dn = float(prices[2])

                    message += (
                        f"{text.split(chr(10))[0]}\n"
                        f"RO: {ro} → {round(ro*0.9,1)}\n"
                        f"BF: {bf} → {round(bf*0.9,1)}\n"
                        f"DN: {dn} → {round(dn*0.9,1)}\n\n"
                    )
            except:
                continue

        if valid_rooms == 0:
            message = "⚠️ No rooms found"

        send_telegram(message)

    except Exception as e:
        send_telegram(f"❌ ERROR:\n{str(e)}")

    finally:
        if driver:
            driver.quit()


def main():
    scrape()


if __name__ == "__main__":
    main()
