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
def home(): return "Saber's Radar is Live!"

def run_web(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# دالة حساب RSI يدوياً (لتجنب المكتبات الثقيلة)
def calculate_rsi(prices, period=14):
    if len(prices) < period: return 50
    gains = []
    losses = []
    for i in range(1, len(prices)):
        change = prices[i] - prices[i-1]
        gains.append(max(change, 0))
        losses.append(max(-change, 0))
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    if avg_loss == 0: return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def get_dashboard_markup():
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("📈 الأسعار الفورية", callback_data='prices'))
    markup.row(InlineKeyboardButton("🎯 فحص الإشارات", callback_data='scan'))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "💎 **أهلاً بك في رادار صابر الاحترافي**\nالنظام جاهز لمراقبة صفقاتك\.", 
                     reply_markup=get_dashboard_markup(), parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "prices":
        p_text = "📊 **الأسعار الحالية:**\n"
        for s in ['BTC/USDT', 'ETH/USDT']:
            ticker = exchange.fetch_ticker(s)
            p_text += f"• {s}: `{ticker['last']}`\n"
        bot.answer_callback_query(call.id)
        bot.edit_message_text(p_text, call.message.chat.id, call.message.message_id, reply_markup=get_dashboard_markup(), parse_mode='Markdown')
    
    elif call.data == "scan":
        bot.answer_callback_query(call.id, "جاري تحليل السوق...")
        # فحص سريع لـ BTC
        ohlcv = exchange.fetch_ohlcv('BTC/USDT', timeframe='1h', limit=20)
        closes = [x[4] for x in ohlcv]
        rsi = calculate_rsi(closes)
        status = "⚖️ متعادل"
        if rsi < 35: status = "🟢 فرصة شراء"
        elif rsi > 65: status = "🔴 فرصة بيع"
        
        msg = f"🔍 **تحليل BTC/USDT:**\n• RSI: `{round(rsi, 2)}`\n• الحالة: *{status}*"
        bot.edit_message_text(msg, call.message.chat.id, call.message.message_id, reply_markup=get_dashboard_markup(), parse_mode='Markdown')

if __name__ == "__main__":
    Thread(target=run_web).start()
    bot.infinity_polling()
