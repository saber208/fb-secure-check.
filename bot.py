import telebot
import ccxt
import pandas as pd
import pandas_ta as ta
import time
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
def home(): return "Trading Radar is Active!"

def run_web(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def get_signal(symbol):
    try:
        bars = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=100)
        df = pd.DataFrame(bars, columns=['time', 'open', 'high', 'low', 'close', 'vol'])
        # حساب مؤشر RSI
        df['RSI'] = ta.rsi(df['close'], length=14)
        last_rsi = df['RSI'].iloc[-1]
        price = df['close'].iloc[-1]
        
        # استراتيجية صابر:
        if last_rsi < 30: # حالة تشبع بيعي (فرصة شراء)
            return f"🟢 **إشارة شراء (Buy)**\nالعملة: {symbol}\nالسعر: {price}\nمؤشر RSI: {round(last_rsi, 2)}\n(السعر رخيص حالياً)"
        elif last_rsi > 70: # حالة تشبع شرائي (فرصة بيع)
            return f"🔴 **إشارة بيع (Sell)**\nالعملة: {symbol}\nالسعر: {price}\nمؤشر RSI: {round(last_rsi, 2)}\n(السعر مرتفع حالياً)"
        return None
    except: return None

def main_loop():
    bot.send_message(ID, "🕵️‍♂️ **بدأتُ الآن بالبحث عن صفقات قوية لك...**")
    symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'AVAX/USDT']
    while True:
        for s in symbols:
            signal = get_signal(s)
            if signal:
                bot.send_message(ID, signal)
        time.sleep(300) # فحص كل 5 دقائق لعدم إزعاجك

if __name__ == "__main__":
    Thread(target=run_web).start()
    main_loop()
