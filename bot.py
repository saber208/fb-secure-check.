import telebot
import ccxt
import time
import os
from flask import Flask
from threading import Thread

# --- إعدادات الحساب ---
TOKEN = '8658226824:AAFF2bfZrsQi4otcYMvHCda9TJea_FKnTJM'
ID = '7716781815'

bot = telebot.TeleBot(TOKEN)
exchange = ccxt.binance({'enableRateLimit': True})
app = Flask('')

@app.route('/')
def home(): return "Saber Pro-Tool is Running!"

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# محرك تحليل الشموع اليابانية
def start_analysis():
    bot.send_message(ID, "🛠️ **تم تفعيل أداة Saber Pro-Pulse داخل التطبيق**\n📉 جاري مراقبة حركة السعر اللحظية...\n🚀 استعد لتنفيذ الصفقات!")
    
    symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'BNB/USDT']
    
    while True:
        for symbol in symbols:
            try:
                # جلب بيانات الشموع لفريم الدقيقة
                bars = exchange.fetch_ohlcv(symbol, timeframe='1m', limit=30)
                closes = [x[4] for x in bars]
                last_price = closes[-1]
                
                # حساب مؤشر القوة النسبية RSI
                diff = [closes[i] - closes[i-1] for i in range(1, len(closes))]
                up = sum([d for d in diff if d > 0])
                down = sum([-d for d in diff if d < 0])
                rsi = 100 - (100 / (1 + (up/down if down != 0 else 1)))

                # منطق الإشارة الاحترافية (مناطق الارتداد)
                if rsi < 14:
                    msg = (f"🟢 **CALL (شراء)**\n\n"
                           f"💎 العملة: {symbol}\n"
                           f"💵 السعر: {last_price}\n"
                           f"⏰ الوقت: 3 دقائق\n"
                           f"⚡ القوة: انفجار سعري للأعلى!")
                    bot.send_message(ID, msg, parse_mode='Markdown')
                    time.sleep(180) # توقف لانتهاء وقت الصفقة

                elif rsi > 86:
                    msg = (f"🔴 **PUT (بيع)**\n\n"
                           f"💎 العملة: {symbol}\n"
                           f"💵 السعر: {last_price}\n"
                           f"⏰ الوقت: 3 دقائق\n"
                           f"⚡ القوة: انفجار سعري للأسفل!")
                    bot.send_message(ID, msg, parse_mode='Markdown')
                    time.sleep(180)

            except: continue
        time.sleep(10) # فحص كل 10 ثوانٍ

if __name__ == "__main__":
    Thread(target=run_web).start()
    # تشغيل الرادار في مسار منفصل لضمان استمراريته
    Thread(target=start_analysis).start()
    bot.infinity_polling()
