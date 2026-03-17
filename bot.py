import telebot
import ccxt
import time
import os
from flask import Flask
from threading import Thread

# --- إعدادات صابر الشخصية ---
TOKEN = '8658226824:AAFF2bfZrsQi4otcYMvHCda9TJea_FKnTJM'
ID = '7716781815'

bot = telebot.TeleBot(TOKEN)
exchange = ccxt.binance()
app = Flask('')

@app.route('/')
def home(): return "Saber Binary System is Online!"

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# دالة تحليل السوق وإرسال الإشارات
def monitor_market():
    # نبدأ برسالة تأكيد عند التشغيل
    bot.send_message(ID, "🚀 **رادار صابر للخيارات الثنائية استيقظ الآن!**\nجاري مراقبة الشموع بدقة 1m\.\.\.")
    
    symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']
    while True:
        for symbol in symbols:
            try:
                # جلب البيانات
                bars = exchange.fetch_ohlcv(symbol, timeframe='1m', limit=20)
                closes = [x[4] for x in bars]
                
                # حساب RSI بسيط وسريع
                up = sum([max(closes[i] - closes[i-1], 0) for i in range(1, len(closes))])
                down = sum([max(closes[i-1] - closes[i], 0) for i in range(1, len(closes))])
                rsi = 100 - (100 / (1 + (up/down if down != 0 else 1)))

                # إرسال الإشارة إذا توفرت الشروط
                if rsi < 18:
                    bot.send_message(ID, f"🟢 **إشارة صعود (CALL)**\n💎 {symbol}\n⏰ المدة: 3 دقائق\n📊 RSI: {round(rsi, 2)}\n✅ ادخل الآن!")
                elif rsi > 82:
                    bot.send_message(ID, f"🔴 **إشارة هبوط (PUT)**\n💎 {symbol}\n⏰ المدة: 3 دقائق\n📊 RSI: {round(rsi, 2)}\n✅ ادخل الآن!")
            except:
                continue
        time.sleep(60) # فحص كل دقيقة

if __name__ == "__main__":
    # تشغيل السيرفر في الخلفية
    Thread(target=run_web).start()
    # تشغيل الرادار في الواجهة الأساسية لمنع توقف البوت
    monitor_market()
