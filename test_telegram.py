from telegram import Bot

BOT_TOKEN = "8868846049:AAE6syp1iH8NXv2y0ehsSBiVJcdLUAmHy3g"
CHAT_ID = 8419437999

print("STARTING TELEGRAM TEST")

bot = Bot(token=BOT_TOKEN)

try:
    response = bot.send_message(
        chat_id=CHAT_ID,
        text="🔥 TEST MESSAGE FROM BOT"
    )
    print("SUCCESS:", response)

except Exception as e:
    print("FAILED:", e)
    raise
