import os
import warnings
import time
import datetime
import logging

import helper.binance
import helper.sqlmanager
# import helper.training
import helper.config
import helper.functions
# import helper.sqlite
import helper.signals
import helper.trade
import helper.telegramsend
import strategies.main

warnings.filterwarnings('ignore')

logger = helper.functions.initlogger("trading_signals.log")

conf = helper.config.initconfig()

CurrencyPairList = ["BTCUSDT","ETHUSDT","BNBUSDT","PAXGUSDT"]

print("Trading Signals start")
logging.info("Trading Signals start")
helper.telegramsend.send("Trading Signals start")

while True:

    os.system('clear')

    time_now = ((int(time.time())*1000))
    print("Aktuelle Zeit: " + str(datetime.datetime.fromtimestamp(time_now/1000)))
    try:
        USDT = helper.binance.get_balance()['free']

        print(USDT, "USDT")
    except Exception as e:
        logging.error("Fehler bei get_balance in trading_signals.py: " + str(e))
        print("Fehler bei get_balance in trading_signals.py: " + str(e))
        time.sleep(60)

    # helper.trade.check_order() TODO

    print()

    # helper.trade.check_filled() TODO

    print()


    timer = datetime.datetime.now().minute

    if timer == 00:
        time.sleep(5)

        for CurrencyPair in CurrencyPairList:
            print()
            print(CurrencyPair)

            data = helper.binance.get_klines_1h(CurrencyPair)

            prepaired_data = helper.signals.prepair_data(data)

            time_minus_45s = ((int(time.time())*1000) - 45000)

            close_time = int(prepaired_data['Close time'].iloc[-2:-1])

            print("Preis:", str(float(prepaired_data['close'].iloc[-2:-1])))

            print("RSI 6: " + str(round(float(prepaired_data['rsi_6'].iloc[-2:-1]),2)))
            print("RSI 12: " + str(round(float(prepaired_data['rsi_12'].iloc[-2:-1]),2)))
            print("RSI 24: " + str(round(float(prepaired_data['rsi_24'].iloc[-2:-1]),2)))
            print("RSI 200: " + str(round(float(prepaired_data['rsi_200'].iloc[-2:-1]),2)))

            print()

            print("SMA 6: " + str(round(float(prepaired_data['sma_6'].iloc[-2:-1]),2)))
            print("SMA 12: " + str(round(float(prepaired_data['sma_12'].iloc[-2:-1]),2)))
            print("SMA 24: " + str(round(float(prepaired_data['sma_24'].iloc[-2:-1]),2)))
            print("SMA 200: " + str(round(float(prepaired_data['sma_200'].iloc[-2:-1]),2)))

            if close_time > time_minus_45s:
                print("Time Treffer")

                # RSI BUY
                data = strategies.main.handler(prepaired_data)
                if data['enter_long'].iloc[-1] == 1:

                    if helper.sqlmanager.get_trade_protectionBuys():
                        logging.info("Buy Trade Time Protection " + CurrencyPair)
                    # TODO Tradeprotection Sells
                    elif helper.trade.getportion(CurrencyPair):
                        logging.info("Buy Portion Protection " + CurrencyPair)
                    else:
                        print("BUY")
                        helper.trade.buy(CurrencyPair) # TODO

        time.sleep(60)

    time.sleep(15)

# docker run -v ./:/mining/ trading_signals
