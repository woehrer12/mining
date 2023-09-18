import os
import warnings
import time
import datetime
import logging

import helper.binance
import helper.predict
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
# CurrencyPairList = helper.predict.pairs()

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

    helper.trade.check_order()

    print()

    helper.trade.check_filled()

    print()


    timer = datetime.datetime.now().minute

    if timer == 00:

        time.sleep(5)

        for CurrencyPair in CurrencyPairList:
            print()
            print(CurrencyPair)

            data = helper.binance.get_klines_1h(CurrencyPair)

            prepaired_data = helper.signals.prepair_data(data)

            print("Preis:", str(float(prepaired_data['close'].iloc[-2:-1])))

            # RSI BUY
            data = strategies.main.handler(prepaired_data)
            if data['enter_long'].iloc[-1] == 1:
                print(data['strategy'])

                if helper.sqlmanager.get_trade_protectionBuys():
                    logging.info("Buy Trade Time Protection " + CurrencyPair)
                elif helper.sqlmanager.get_trade_protectionSells():
                    logging.info("Buy Trade Time Protection Sells " + CurrencyPair)
                # TODO Portion
                else:
                    print("BUY")
                    helper.trade.buy(CurrencyPair, float(conf['set_size']))

        time.sleep(60)

    time.sleep(15)

# docker run -v ./:/mining/ trading_signals
