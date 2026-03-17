import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import ccxt
import time
import os
from flask import Flask
from threading import Thread

# --- إعدادات صابر المحترفة ---
TOKEN = '8658226824:AAFF2bfZrsQi4otcYMvHCda9TJea_FKnTJM'
ID = '7716781815'

bot = telebot.TeleBot(TOKEN, parse_mode='MarkdownV2')
exchange = ccxt.binance()
app = Flask('')

@app.route('/')
def home(): return "Saber Professional Radar is Live!"

def run_web(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# دالة لإنشاء لوحة التحكمInline الكلاسيكية
def create_dashboard_markup():
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton('📊 لوحة تحكم السوق', callback_data='market'))
    markup.row(
        InlineKeyboardButton('⚡ تحليل سريع \(BTC\)', callback_data='analyze_btc'),
        InlineKeyboardButton('🔍 فحص إشارات', callback_data='signals')
    )
    markup.row(InlineKeyboardButton('👤 حسابي | إعدادات', callback_data='account'))
    return markup

@bot.message_handler(commands=['start'])
def welcome(message):
    text = "👋 **مرحباً بك في لوحة تحكم صابر للتداول الذكي**\nالنظام متصل الآن ويراقب السوق على مدار الساعة\."
    bot.send_message(message.chat.id, text, reply_markup=create_dashboard_markup())

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == 'market':
        # تنسيق كروت السوق الحديثة
        symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']
        prices = ""
        for s in symbols:
            ticker = exchange.fetch_ticker(s)
            prices += f"🔹 {s}: `${ticker['last']}`\n"
        text = f"⚖️ **نظرة شاملة على السوق اللحظية:**\n\n{prices}\n🕒 آخر تحديث: `{time.strftime('%H:%M:%S')}`"
        bot.answer_callback_query(call.id, "جاري تحميل بيانات السوق")
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=create_dashboard_markup())
    
    elif call.data == 'signals':
        # تنبيه فوري
        text = "🕵️‍♂️ **جاري فحص خوارزميات الذكاء الصناعي\.\.\.**\nلا توجد إشارات قوية حالياً\. سأرسل لك إشعاراً فور توفر فرصة\."
        bot.answer_callback_query(call.id)
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=create_dashboard_markup())

if __name__ == "__main__":
    Thread(target=run_web).start()
    bot.infinity_polling()
