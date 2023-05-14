from binance.client import Client
from binance.enums import *

import helper.config

conf = helper.config.initconfig()

client = Client(conf['binance_api_key'], conf['binance_api_secret'])

def ping():
    return client.ping()

def get_server_time():
    return client.get_server_time()

def get_system_status():
    return client.get_system_status()

def get_exchange_info():
    return client.get_exchange_info()

def get_symbol_info(CurrencyPair):
    return client.get_symbol_info(CurrencyPair)

def get_24h_ticker():
    return client.get_ticker()

def get_avg_price(CurrencyPair):
    return client.get_avg_price(symbol=CurrencyPair)

def get_all_tickers():
    return client.get_all_tickers()

def get_balance():
    return client.get_asset_balance(asset='USDT')

def get_balance_pair(CurrencyPair):
    CurrencyPair = CurrencyPair.replace("USDT", "")
    return client.get_asset_balance(asset=CurrencyPair)

def limit_buy(symbol, quantity, price, test):
    if test == 1:
        return client.create_test_order(symbol=symbol, side=SIDE_BUY, type=ORDER_TYPE_LIMIT, timeInForce=TIME_IN_FORCE_GTC, quantity=quantity, price=price)
    return client.order_limit_buy(symbol=symbol, quantity=quantity, price=price)

def limit_sell(symbol, quantity, price):
    return client.order_limit_sell(symbol=symbol, quantity=quantity, price=price)

def check_order(CurrencyPair, orderId):
    return client.get_order(symbol=CurrencyPair,orderId=orderId)

def cancel_order(CurrencyPair, orderId):
    return client.cancel_order(symbol=CurrencyPair,orderId=orderId)

def market_buy(symbol, quantity):
    return client.order_market_buy(symbol=symbol, quantity=quantity)

def market_sell(symbol, quantity):
    return client.order_market_sell(symbol=symbol, quantity=quantity)

def get_klines_1h(symbol):
    return client.get_klines(symbol = symbol, interval = Client.KLINE_INTERVAL_1HOUR)

def get_klines_15m(symbol):
    return client.get_klines(symbol = symbol, interval = Client.KLINE_INTERVAL_15MINUTE)

def get_historical_klines_1h(symbol):
    return client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1HOUR,"1 Jan, 2017")

def get_historical_klines_15m(symbol):
    return client.get_historical_klines(symbol, Client.KLINE_INTERVAL_15MINUTE,"1 Jan, 2017")

def get_historical_klines_start(symbol,start):
    return client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1MINUTE, start)
