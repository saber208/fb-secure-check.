import ccxt
import pandas as pd
import pandas_ta as ta
import time
import telebot

# --- بيانات صابر الموثقة (أمان 100%) ---
TOKEN = '8658226824:AAFF2bfZrsQi4otcYMvHCda9TJea_FKnTJM'
ID = '7716781815'

bot = telebot.TeleBot(TOKEN)
# استخدام منصة Binance لجلب أسعار الدولار (USDT)
exchange = ccxt.binance()

# العملات التي سيراقبها الرادار (يمكنك زيادة القائمة لاحقاً)
symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'BNB/USDT', 'LTC/USDT', 'AVAX/USDT']

def fetch_and_scan(symbol):
    try:
        # جلب بيانات الشموع (إطار 15 دقيقة لتحليل سريع ودقيق)
        bars = exchange.fetch_ohlcv(symbol, timeframe='15m', limit=100)
        df = pd.DataFrame(bars, columns=['ts', 'open', 'high', 'low', 'close', 'vol'])
        
        # حساب مؤشر القوة النسبية (RSI) - المحرك العلمي للبوت
        df['RSI'] = ta.rsi(df['close'], length=14)
        current_rsi = df['RSI'].iloc[-1]
        current_price = df['close'].iloc[-1]

        # --- منطق الإشعارات الفورية ---
        
        # 🟢 حالة الشراء (السعر رخيص جداً علمياً)
        if current_rsi < 30:
            msg = f"🟢 **إشارة شراء ذهبية!**\n💎 العملة: {symbol}\n💰 السعر: {current_price}$\n📉 مؤشر RSI: {current_rsi:.2f}\n⚠️ الحالة: منطقة تشبع بيعي (قاع)"
            bot.send_message(ID, msg, parse_mode='Markdown')
        
        # 🔴 حالة البيع (السعر مرتفع جداً علمياً)
        elif current_rsi > 70:
            msg = f"🔴 **إشارة جني أرباح!**\n💎 العملة: {symbol}\n💰 السعر: {current_price}$\n📈 مؤشر RSI: {current_rsi:.2f}\n⚠️ الحالة: منطقة تشبع شرائي (قمة)"
            bot.send_message(ID, msg, parse_mode='Markdown')

    except Exception as e:
        print(f"حدث خطأ في مراقبة {symbol}: {e}")

def main():
    # رسالة ترحيبية عند التشغيل
    bot.send_message(ID, "🚀 **نظام رادار صابر العلمي يعمل الآن..**\nأنا أراقب السوق لك 24 ساعة، سأخبرك فور وجود فرصة شراء بالدولار!")
    
    while True:
        for s in symbols:
            fetch_and_scan(s)
            time.sleep(2) # حماية السيرفر وتجنب الحظر
        
        # إعادة فحص السوق بالكامل كل 5 دقائق
        time.sleep(300)

if __name__ == "__main__":
    main()
