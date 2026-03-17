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
# استخدام منصة جلب بيانات شاملة
exchange = ccxt.binance({'enableRateLimit': True})
app = Flask('')

@app.route('/')
def home(): return "Binary Elite Radar is Active!"

def run_web(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def check_signals():
    # مراقبة العملات الرقمية والذهب (عبر Binance)
    symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']
    while True:
        for symbol in symbols:
            try:
                bars = exchange.fetch_ohlcv(symbol, timeframe='1m', limit=25)
                closes = [x[4] for x in bars]
                
                # استراتيجية القوة النسبية المطورة
                up = sum([max(closes[i] - closes[i-1], 0) for i in range(1, len(closes))])
                down = sum([max(closes[i-1] - closes[i], 0) for i in range(1, len(closes))])
                rsi = 100 - (100 / (1 + (up/down if down != 0 else 1)))

                # إشارة CALL (صعود)
                if rsi < 18:
                    msg = f"🟢 **إشارة صعود (CALL)**\n\n💎 {symbol}\n⏰ المدة: 3 - 5 دقائق\n📊 القوة: مرتفعة\n🚀 ادخل الآن!"
                    bot.send_message(ID, msg, parse_mode='Markdown')
                
                # إشارة PUT (هبوط)
                elif rsi > 82:
                    msg = f"🔴 **إشارة هبوط (PUT)**\n\n💎 {symbol}\n⏰ المدة: 3 - 5 دقائق\n📊 القوة: مرتفعة\n📉 ادخل الآن!"
                    bot.send_message(ID, msg, parse_mode='Markdown')
            except: continue
        time.sleep(60)

if __name__ == "__main__":
    Thread(target=run_web).start()
    Thread(target=check_signals).start()
    bot.send_message(ID, "💎 **تم تفعيل رادار الخيارات الثنائية بنجاح!**\nسأقوم بتنبيهك فوراً عند وجود فرصة دخول قوية\.")
    bot.infinity_polling()

        
