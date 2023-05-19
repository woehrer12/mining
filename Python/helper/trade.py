import datetime
import time
import logging

import helper.binance
import helper.sqlmanager
import helper.telegramsend
import helper.functions
import helper.config
import numpy as np
from binance.helpers import round_step_size

conf = helper.config.initconfig()

helper.sqlmanager.init()

kinds = ["Slow", "Middle"]#, "Fast"]

def buy(CurrencyPair, Size):
    USDT = float(helper.binance.get_balance()['free'])
    print("USDT: " + USDT)
    for kind in kinds:
        if float(USDT) > (Size * 1.01) + float(conf['reserve']) :
            print(kind)
            price = helper.binance.get_24h_ticker()
            for dict in price:
                if dict['symbol'] == CurrencyPair:
                    price = float(dict['lastPrice'])*0.9999

            ticksize = helper.binance.get_symbol_info(CurrencyPair)['filters'][0]['tickSize']
            stepsize = helper.binance.get_symbol_info(CurrencyPair)['filters'][1]['stepSize'] # TODO Change to 1 Request

            Size = round(1/float(price)*Size,8)
            price = round_step_size(float(price),ticksize)
            price = '{0:.8f}'.format(price)
            print("Preis: " + str(price))

            Size = round_step_size(Size,stepsize)
            print("Menge: "+ str(Size))
            logging.info("CurrencyPair: "+ str(CurrencyPair) + " Size: " + str(Size) + " Price: " + str(price))
            result = helper.binance.limit_buy(CurrencyPair, Size, price, 0)
            result['status'] = 'NEW'
            helper.sqlmanager.insert_buy(result,kind)
            USDT = USDT - Size * 1.01
            logging.info("Buy ")
            logging.info(result)
        else:
            print("Not Enougth USDT")

def sell(Id):
    # Search the Orders in Database
    trade = helper.sqlmanager.search_id(Id)

    # Get the actual prices
    price = helper.binance.get_24h_ticker()
    for dict in price:
        if dict['symbol'] == trade.symbol:
            price = float(dict['lastPrice'])*1.0001

    # Get the symbol infos for the right values in trade request
    ticksize = helper.binance.get_symbol_info(trade.symbol)['filters'][0]['tickSize']
    stepsize = helper.binance.get_symbol_info(trade.symbol)['filters'][1]['stepSize'] # TODO change to 1 Request

    price = round_step_size(float(price),ticksize)
    profit = float(((price/trade.price)*100)-100)
    price = '{0:.8f}'.format(price)
    print("Preis: " + str(price))
    
    size = float(trade[7]) * (1.0-(profit/100.0*0.2))
    size = round_step_size(size,stepsize)
    print("Menge: "+ str(size))
    print("Profit: " + str(round(profit,2)) + "%")
    
    logging.info("SELL: " + str(trade.symbol) + ", size: " + str(size) + ", price: " + str(price))

    # Set the Sell Request
    result = helper.binance.limit_sell(trade[0], size, price)

    result['status'] = 'NEW'

    # Insert into Databse
    helper.sqlmanager.update_buys_Sell_id(result, trade.trade_id)

    # Logging
    logging.info("SELL")
    logging.info(trade)
    logging.info(result)
    logging.info("Size: " + str(size))
    logging.info("Price: " + str(price))




def check_order():
    try:
        print("Check order")
        trades = helper.sqlmanager.search_new_buys()
        for trade in trades:
            result = helper.binance.check_order(trade.symbol,trade.orderid)
            if result['status'] == "FILLED":
                helper.sqlmanager.update_buys(result, trade.trade_id)
                logging.info("Buy complete")
                logging.info(result)
                helper.telegramsend.send("BUY " + str(trade.symbol) + " Price: " + str(trade.price))
            else:
                time_now = int(time.time())*1000
                time_cancel = int(time_now - 3300000)
                trade_time = int(trade.transactTime)
                if trade_time < time_cancel:
                    print("CANCEL")
                    cancel_orderBuys(trade.trade_id, result)
                    logging.info("Cancel Buy")
                    logging.info(trade)
    except Exception as e:
        logging.error("Fehler bei checkorder open BUY in trade.py: " + str(e))
        print("Fehler bei checkorder in trade.py: " + str(e))
        time.sleep(60)

    try:
        trades = helper.sqlmanager.search_new_sells()
        for trade in trades:
            print(trade.trade_id)
            print(trade.symbol)
            result = helper.binance.check_order(trade.symbol,trade.orderid)
            if result['status'] == "FILLED":
                helper.sqlmanager.update_buys_Sell_status(result['status'], trade.trade_id)
                profit = float(((trade.price/result['price'])*100)-100)
                profit_USDT = float(result['cummulativeQuoteQty']) - trade.executedQty
                logging.info("Sell complete")
                logging.info(trade)
                helper.telegramsend.send("SELL " + str(trade.symbol) + " Price: " + str(trade.price) + " Profit: " + str(round(profit,2)) + " USDT: " + str(round(profit_USDT,2)))
            else:
                time_now = int(time.time())*1000
                time_cancel = int(time_now - 3300000)
                trade_time = int(trade.transactTime)
                print("Pair: " + str(trade.symbol) + "  Price: " + str(trade.price) + "  Menge: " + str(trade.executedQty) + "  Time: " + str(datetime.datetime.fromtimestamp(trade.transacttime/1000)))
                if trade_time < time_cancel:
                    print("CANCEL")
                    logging.info("Cancel Sell")
                    logging.info(trade)
                    cancel_orderSells(result, trade[13])
    except Exception as e:
        logging.error("Fehler bei checkorder open SELL in trade.py: " + str(e))
        print("Fehler bei checkorder in trade.py: " + str(e))
        time.sleep(60)
        




def check_filled():
    try:
        print("Check filled")
        trades = helper.sqlmanager.search_filled_buys()
        price_dict = helper.binance.get_24h_ticker()
        arr = []
        arr_w = []
        arrUSDT = []
        for trade in trades:
            for dict in price_dict:
                if dict['symbol'] == trade.symbol:
                    price = float(dict['lastPrice'])
            print("Preis: ",price)

            arr = np.append(arr,trade.price)
            arr_w = np.append(arr_w,trade.executedQty)
            arrUSDT = np.append(arrUSDT,trade.executedQty)
            profit = float(((price/trade.price)*100)-100)

            if trade.kind == "Fast":
                trailingvalue = 1.0
                trailingoffset = 2.0
            elif trade.kind == "Middle":
                trailingvalue = 2.5
                trailingoffset = 5.0
            else:
                trailingvalue = 5.0
                trailingoffset = 10.0
            
            if profit > trailingoffset:
                if not trade.trailingProfit:
                    trailing = profit - trailingvalue
                    helper.sqlmanager.update_trailing(trade.trade_id,trailing)
                else: 
                    if profit > trade.trailingProfit + trailingvalue:
                        trailing = profit - trailingvalue
                        helper.sqlmanager.update_trailing(trade.trade_id,trailing)
            if not(not trade.trailingProfit):
                if profit > 2.0:
                    if profit < trade.trailingProfit:
                        Coins = float(helper.binance.get_balance_pair(trade[0])['free'])
                        if helper.sqlmanager.get_trade_protectionBuys():
                            logging.info("Sell Trade Time Protection")
                            logging.info(trade)
                        if helper.sqlmanager.get_trade_protectionSells():
                            logging.info("Sell Trade Time Protection Sell")
                            logging.info(trade)
                        elif trade.executedQty > Coins:
                            logging.info("Sell Trade Balance Protection")
                            logging.info(trade)
                            helper.sqlmanager.update_trailing_to_null(trade.trade_id,trailing)
                            logging.info("Set TradetoNULL")
                            logging.info(trade)
                            helper.telegramsend.send("Not Enought for Sell" + str(trade[0]) + " ID:" + str(trade[15]))
                        else:
                            print("SELL")
                            sell(trade.trade_id)
                else:
                    helper.sqlmanager.update_trailing_to_null(trade.trade_id,trailing)
                    logging.info("Set TradetoNULL")
                    logging.info(trade)
                    helper.telegramsend.send("Reset Trailing while under 2%" + str(trade[0]) + " ID:" + str(trade[15]))
        if len(arr) >0:
            gewichteter_durchschnitt = np.average(arr,weights = arr_w)
            profit = float(((price/gewichteter_durchschnitt)*100)-100)
            print("Gewichteter Durchschnitt : ", round(gewichteter_durchschnitt,2))
            print("Summe: ", np.sum(arr_w))
            print("Summe: ", round(np.sum(arrUSDT),2), "USDT")
            print("Durschnittlicher Gewinn: " + str(round(profit,2)) + "%")
            print()
    except Exception as e:
        logging.error("Fehler bei check_filled in trade.py: " + str(e))
        print("Fehler bei check_filled in trade.py: " + str(e))
        time.sleep(60)

def cancel_orderBuys(trade_id,data):
    try:
        print(data)
        helper.binance.cancel_order(data['symbol'],data['orderId'])
        helper.sqlmanager.delete_buys(trade_id)
    except Exception as e:
        logging.error("Fehler bei cancel_order Buys in trade.py: " + str(e))
        print("Fehler bei cancel_order Buys in trade.py: " + str(e))
        time.sleep(60)

def cancel_orderSells(data, buyId):
    print(data)
    try:
        helper.binance.cancel_order(data['symbol'],data['orderId'])
        helper.sqlmanager.update_delete_sell(buyId, "")
    except Exception as e:
        logging.error("Fehler bei cancel_orderSells in trade.py: " + str(e))
        print("Fehler bei cancel_orderSells in trade.py: " + str(e))
        time.sleep(60)
