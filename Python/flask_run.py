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
    

    return render_template('<h1>You are wronh here</h1>')




@app.route('/sell')
def sell():
    Id = request.args.get('Id')
    helper.trade.sell(Id)
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
