from telegram import Bot

BOT_TOKEN = "8752290947:AAGdhXELc0JY3ZTiJO9xwNJcD2O0k1pIo4w"
CHAT_ID = 8752290947

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
