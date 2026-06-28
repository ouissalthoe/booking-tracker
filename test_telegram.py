import requests

BOT_TOKEN = "8752290947:AAGdhXELc0JY3ZTiJO9xwNJcD2O0k1pIo4w"
CHAT_ID = "8419437999"

message = "🔥 GitHub test message"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

payload = {
    "chat_id": CHAT_ID,
    "text": message
}

response = requests.post(url, data=payload)

print("STATUS:", response.status_code)
print("RESPONSE:", response.text)
