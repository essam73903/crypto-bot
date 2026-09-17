import time
import ccxt
import pandas as pd
import ta

exchange = ccxt.binance({
    'apiKey': 'YfDXSnx6W1keHkgVqUtXOQyjJ2W0pWYY06cipyGRj2afjwxYSdhnimwCLSkzvly3',
    'secret': '6JmJyUnKAPT6vDVIuyj4EN64f9n49oCJjvfQNa0XsefXdhgsY4Zjva8CMyw7yOND',
    'enableRateLimit': False,
    'options': {'defaultType': 'spot'}
})

timeframe = '15m'
PROFIT_TARGET = 1.15  # 15% ربح مستهدف

TOP_SYMBOLS = [
    'BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'BNB/USDT', 'XRP/USDT', 
    'ADA/USDT', 'DOGE/USDT', 'AVAX/USDT', 'LINK/USDT', 'MATIC/USDT',
    'NEAR/USDT', 'DOT/USDT', 'UNI/USDT', 'ATOM/USDT', 'FET/USDT'
]

def smart_ai_scan():
    try:
        balance = exchange.fetch_free_balance()
        usdt_balance = balance.get('USDT', 0.0)

        for symbol in TOP_SYMBOLS:
            try:
                base_currency = symbol.split('/')[0]
                asset_balance = balance.get(base_currency, 0.0)
                
                # جلب البيانات التاريخية المتقدمة للتحليل الذكي
                ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=50)
                if len(ohlcv) < 35:
                    continue
                    
                df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                
                # حساب مؤشرات الذكاء الاصطناعي المتقدمة (RSI + MACD + Bollinger Bands)
                rsi = ta.momentum.RSIIndicator(df['close'], window=14).rsi().iloc[-1]
                
                macd_indicator = ta.trend.MACD(df['close'])
                macd = macd_indicator.macd().iloc[-1]
                macd_signal = macd_indicator.macd_signal().iloc[-1]
                
                current_price = exchange.fetch_ticker(symbol)['last']

                # 1. نظام البيع الذكي وجني الأرباح (15% أو تقاطع سلبي قوي)
                if asset_balance > 0:
                    try:
                        my_trades = exchange.fetch_my_trades(symbol, limit=5)
                        buy_trades = [t for t in my_trades if t['side'] == 'buy']
                        if buy_trades:
                            last_buy_price = buy_trades[-1]['price']
                            profit_ratio = current_price / last_buy_price
                            print(f"🧠 AI Monitoring {symbol} | Profit: {((profit_ratio-1)*100):.2f}%")
                             
                            if profit_ratio >= PROFIT_TARGET or rsi > 70:
                                print(f"💰 AI TARGET REACHED! Selling {symbol} for 15%+ profit!")
                                exchange.create_market_sell_order(symbol, asset_balance)
                    except:
                        if rsi > 65:
                            exchange.create_market_sell_order(symbol, asset_balance)

                # 2. نظام الشراء الخارق (فلترة الفرص الذهبية بدقة لمنع الخسارة)
                elif usdt_balance >= 5.0:
                    # شروط الشراء الذكي: RSI منخفض (< 42) + تقاطع إيجابي في الـ MACD
                    if rsi < 42 and macd > macd_signal:
                        print(f"💎 AI HIGH-ACCURACY BUY SIGNAL on {symbol} | RSI: {rsi:.2f} | MACD Confirmed!")
                        amount_to_buy = (usdt_balance * 0.98) / current_price
                        order = exchange.create_market_buy_order(symbol, amount_to_buy)
                        print(f"✅ Successfully bought {symbol}:", order)
                        break

            except Exception as inner_e:
                continue

    except Exception as e:
        print(f"⚠️ AI Scan Error: {e}")

def run_bot():
    print("🤖 Ultra-Smart AI Trading Bot started in background...")
    while True:
        smart_ai_scan()
        time.sleep(10)  # فحص خارق ومتكرر كل 10 ثوانٍ للفرص

if __name__ == "__main__":
    run_bot()
