from telegram import Bot

BOT_TOKEN = "8868846049:AAE6syp1iH8NXv2y0ehsSBiVJcdLUAmHy3g"
CHAT_ID = 8419437999

bot = Bot(token=BOT_TOKEN)
bot.send_message(chat_id=CHAT_ID, text="🔥 TEST MESSAGE")
print("sent")
