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
    helper.sqlmanager.updateBuywithSellid(result['orderId'], trade.trade_id)

    # Logging
    logging.info("SELL")
    logging.info(trade)
    logging.info(result)
    logging.info("Size: " + str(size))
    logging.info("Price: " + str(price))




def check_order():
    try:
        print()
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
                    cancel_orderBuys(result)
                    logging.info("Cancel Buy")
                    logging.info(trade)
    except Exception as e:
        logging.error("Fehler bei checkorder open BUY in trade.py: " + str(e))
        print("Fehler bei checkorder in trade.py: " + str(e))
        time.sleep(60)

    try:
        trades = helper.sqlmanager.get_trade_protectionBuys()
        for trade in trades:
            result = helper.binance.check_order(trade.symbol,trade.orderid)
            if result['status'] == "FILLED":
                helper.sqlmanager.updateSellTrade(result)
                buytrade = helper.sqlite.getSearchorderId2(trade[13])
                profit = float(((trade[5]/buytrade[5])*100)-100)
                profit_USDT = float(result['cummulativeQuoteQty']) - buytrade[8]
                helper.sqlite.insertProfit(trade[0], trade[13], trade[14], profit, profit_USDT)
                logging.info("Sell complete")
                logging.info(trade)
                logging.info(buytrade)
                helper.telegramsend.send("SELL " + str(trade[0]) + " Price: " + str(trade[5]) + " Profit: " + str(round(profit,2)) + " USDT: " + str(round(profit_USDT,2)))
            else:
                time_now = int(time.time())*1000
                time_cancel = int(time_now - 3300000)
                trade_time = int(trade[4])
                print("Pair: " + str(trade[0]) + "  Price: " + str(trade[5]) + "  Menge: " + str(trade[6]) + "  Time: " + str(datetime.datetime.fromtimestamp(trade[4]/1000)))
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

            arr = np.append(arr,trade[5])
            arr_w = np.append(arr_w,trade[6])
            arrUSDT = np.append(arrUSDT,trade[8])
            profit = float(((price/trade[5])*100)-100)

            if trade[16] == "Fast":
                trailingvalue = 1.0
                trailingoffset = 2.0
            elif trade[16] == "Middle":
                trailingvalue = 2.5
                trailingoffset = 5.0
            else:
                trailingvalue = 5.0
                trailingoffset = 10.0
            
            if profit > trailingoffset:
                if not trade[14]:
                    trailing = profit - trailingvalue
                    helper.sqlite.updateTrailingTrade(trade[1],trailing)
                else: 
                    if profit > trade[14] + trailingvalue:
                        trailing = profit - trailingvalue
                        helper.sqlite.updateTrailingTrade(trade[1],trailing)
            if not(not trade[14]):
                if profit > 2.0:
                    if profit < trade[14]:
                        Coins = float(helper.binance.get_balance_pair(trade[0])['free'])
                        if helper.sqlite.gettradeprotection():
                            logging.info("Sell Trade Time Protection")
                            logging.info(trade)
                        elif trade[6] > Coins:
                            logging.info("Sell Trade Balance Protection")
                            logging.info(trade)
                            helper.sqlite.updateTrailingTradetoNULL(trade[1])
                            logging.info("Set TradetoNULL")
                            logging.info(trade)
                            helper.telegramsend.send("Not Enought for Sell" + str(trade[0]) + " ID:" + str(trade[15]))
                        else:
                            print("SELL")
                            sell2(trade[15])
                else:
                    helper.sqlite.updateTrailingTradetoNULL(trade[1])
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

def cancel_orderBuys(data):
    try:
        helper.binance.cancel_order(data['symbol'],data['orderId'])
        helper.sqlite.deleteBuyTrade(data)
    except Exception as e:
        logging.error("Fehler bei cancel_orderSells in trade.py: " + str(e))
        print("Fehler bei cancel_orderSells in trade.py: " + str(e))
        time.sleep(60)

def cancel_orderSells(data, buyId):
    try:
        helper.binance.cancel_order(data['symbol'],data['orderId'])
        helper.sqlite.updateBuywithSellid(buyId, "")
        helper.sqlite.deleteSellTrade(data)
    except Exception as e:
        logging.error("Fehler bei cancel_orderSells in trade.py: " + str(e))
        print("Fehler bei cancel_orderSells in trade.py: " + str(e))
        time.sleep(60)

def getportion(CurrencyPair):
    allopenTrades = helper.sqlite.getSearchFilledBuysall()

    USDT = 0.0
    totalUSDT = 0.0
    for Trade in allopenTrades:
        Trade = list(Trade)
        if Trade[0] == CurrencyPair:
            USDT += Trade[8]
        totalUSDT += Trade[8]

    portion = USDT/ totalUSDT * 100.0
    if portion > 40:
        logging.info("Get Portion: " + str(portion) + " " + str(CurrencyPair) + " USDT: " + str(USDT) + " totalUSDT: " + str(totalUSDT))
        return True
    return False