from flask import Flask , render_template, request

import helper.sqlmanager
import helper.functions
import helper.config
import helper.binance
import helper.trade

import logging
import os
import datetime
import numpy as np
import logging

app = Flask(__name__)

logger = helper.functions.initlogger("flask_run.log")

conf = helper.config.initconfig()

print("Flask start")
logging.info("Flask start")

def Sort(sub_li):
    sub_li.sort(key = lambda x: x[17],reverse=True)
    return sub_li



@app.route('/')
def index():
    binanceprice = helper.binance.get_24h_ticker()
    USDT = float(helper.binance.get_balance()['free'])
    

    return render_template('index.html',    allopenTrades=allTrades2, 
                                            allopenBuys=allBuys2, 
                                            allopenSells=allSells2, 
                                            USDT=USDT, 
                                            totalprofitUSDT=totalprofitUSDT,
                                            totalUSDT=totalUSDT,
                                            BTC=BTC,
                                            ETH=ETH,
                                            BNB=BNB,
                                            PAXG=PAXG)


@app.route('/trade')
def trade():
    Id = request.args.get('Id')
    Trade = helper.sqlmanager.getSearchorderId2(Id)
    Trade = list(Trade)
    Trade.transactTime = datetime.datetime.fromtimestamp(Trade.transactTime/1000).strftime("%d.%m.%Y %H:%M:%S")
    binanceprice = helper.binance.get_24h_ticker()
    for dict in binanceprice:
        if dict['symbol'] == Trade.symbol:
            price = float(dict['lastPrice'])
    profit = float(((price/Trade[5])*100)-100)
    Trade.append(str(round(profit,2)))
    return render_template('trade.html', Trade=Trade)


@app.route('/sell')
def sell():
    Id = request.args.get('Id')
    helper.trade.sell2(Id)
    return "<h1>SELL {}".format(Id)

@app.route('/buy')
def buy():
    Pair = request.args.get('Pair')
    Size = request.args.get('Size')
    logging.info("Buying {} with size {}".format(Pair, Size))
    helper.trade.buy(Pair, float(Size))
    return "<h1>BUY {}".format(Pair)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


app.run(host='0.0.0.0', debug=True, port=5001)
