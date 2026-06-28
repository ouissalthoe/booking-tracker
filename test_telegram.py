import requests


BOT_TOKEN = "8868846049:AAE6syp1iH8NXv2y0ehsSBiVJcdLUAmHy3g"
CHAT_ID = 8419437999

message = "🔥 TEST MESSAGE FROM GITHUB"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

payload = {
    "chat_id": CHAT_ID,
    "text": message
}

response = requests.post(url, data=payload)

print("STATUS CODE:", response.status_code)
print("RESPONSE:", response.text)
