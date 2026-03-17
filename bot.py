import telebot
import os
from flask import Flask
from threading import Thread

# بيانات صابر (أمان كامل)
TOKEN = '8658226824:AAFF2bfZrsQi4otcYMvHCda9TJea_FKnTJM'
ID = '7716781815'

bot = telebot.TeleBot(TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    # هذا السطر يحل مشكلة الـ Port في Render
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

if __name__ == "__main__":
    # تشغيل سيرفر الويب في خلفية الكود
    t = Thread(target=run)
    t.start()
    
    try:
        print("Starting Bot...")
        bot.send_message(ID, "🚀 **رادار صابر العلمي استيقظ الآن وهو يراقب السوق!**")
        bot.infinity_polling()
    except Exception as e:
        print(f"Error: {e}")

