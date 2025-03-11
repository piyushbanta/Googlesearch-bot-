import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# अपने बॉट का टोकन यहाँ डालें
TELEGRAM_BOT_TOKEN = "7932342839:AAGMEZJYflcjrFqK0BTGZaLRuPae9dv7tcI"
SERPAPI_KEY = "f61f2fc0f10ba41300a0a0d7776ea423d204cf371b78501172e8b17aaacf72bb"

# लॉगिंग सेटअप
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# गूगल सर्च फंक्शन
def google_search(query):
    url = f"https://serpapi.com/search.json?q={query}&api_key={SERPAPI_KEY}"
    response = requests.get(url)
    data = response.json()
    
    # पहला परिणाम निकालें
    if "organic_results" in data and len(data["organic_results"]) > 0:
        result = data["organic_results"][0]
        return f"{result['title']}\n{result['link']}\n\n{result['snippet']}"
    return "मुझे कोई सटीक जानकारी नहीं मिली।"

# /start कमांड हैंडलर
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("नमस्ते! मैं एक गूगल सर्च बॉट हूँ। आप मुझसे कुछ भी पूछ सकते हैं।")

# सामान्य मैसेज हैंडलर (सवालों के उत्तर देने के लिए)
async def handle_message(update: Update, context: CallbackContext):
    query = update.message.text
    answer = google_search(query)
    await update.message.reply_text(answer)

# मेन फंक्शन
def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("बॉट चालू है...")
    app.run_polling()

if __name__ == "__main__":
    main()