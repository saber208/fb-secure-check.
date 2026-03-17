import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import ccxt
import os
from flask import Flask
from threading import Thread

# --- إعدادات صابر ---
TOKEN = '8658226824:AAFF2bfZrsQi4otcYMvHCda9TJea_FKnTJM'
ID = '7716781815'

bot = telebot.TeleBot(TOKEN)
exchange = ccxt.binance()
app = Flask('')

@app.route('/')
def home(): return "Saber Dashboard is Active!"

def run_web(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# دالة حساب RSI يدوياً وبسرعة
def get_rsi(symbol):
    try:
        bars = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=20)
        closes = [x[4] for x in bars]
        deltas = [closes[i] - closes[i-1] for i in range(1, len(closes))]
        gains = [d for d in deltas if d > 0]
        losses = [-d for d in deltas if d < 0]
        avg_gain = sum(gains) / 14
        avg_loss = sum(losses) / 14
        if avg_loss == 0: return 100
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))
    except: return 50

def get_menu():
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("📈 تحديث الأسعار", callback_data='prices'))
    markup.row(InlineKeyboardButton("🎯 فحص الصفقات", callback_data='scan'))
    return markup

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "🚀 **رادار صابر المطور جاهز!**\nاضغط على الأزرار بالأسفل:", reply_markup=get_menu(), parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: True)
def handle_click(call):
    # إبلاغ تليجرام أننا استلمنا الضغطة فوراً (تزيل التحميل)
    bot.answer_callback_query(call.id)
    
    if call.data == 'prices':
        try:
            btc = exchange.fetch_ticker('BTC/USDT')['last']
            eth = exchange.fetch_ticker('ETH/USDT')['last']
            text = f"📊 **الأسعار اللحظية:**\n• BTC: `${btc}`\n• ETH: `${eth}`"
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=get_menu(), parse_mode='Markdown')
        except:
            bot.send_message(call.message.chat.id, "⚠️ خطأ في الاتصال ببينانس")

    elif call.data == 'scan':
        bot.edit_message_text("🔍 جاري التحليل الرقمي...", call.message.chat.id, call.message.message_id)
        rsi = get_rsi('BTC/USDT')
        status = "⚖️ مستقر"
        if rsi < 35: status = "🟢 فرصة شراء قوية"
        elif rsi > 65: status = "🔴 فرصة بيع قوية"
        
        res = f"🎯 **تحليل الـ BTC:**\n• RSI: `{round(rsi, 2)}`\n• الحالة: *{status}*"
        bot.edit_message_text(res, call.message.chat.id, call.message.message_id, reply_markup=get_menu(), parse_mode='Markdown')

if __name__ == "__main__":
    Thread(target=run_web).start()
    bot.infinity_polling()
