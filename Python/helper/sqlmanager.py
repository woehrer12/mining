import sqlalchemy as db
import time

import helper.config

conf = helper.config.initconfig()

connection_string = "mysql+mysqlconnector://" + conf['MYSQL_USER'] + ":" + conf['MYSQL_PASS'] + "@" + conf['MYSQL_HOST'] + ":3306/sqlalchemy"

engine = db.create_engine(connection_string, echo=True)
metadata = db.MetaData()

Buys = db.Table('Buys', metadata,
            db.Column('trade_id', db.Integer(),primary_key = True),
            db.Column('symbol', db.String(8), nullable = False),
            db.Column('orderid', db.Integer),
            db.Column('orderListId', db.Integer),
            db.Column('clientOrderId', db.String(12)),
            db.Column('transactTime', db.Integer),
            db.Column('price', db.Float),
            db.Column('origQty', db.Float),
            db.Column('executedQty', db.Float),
            db.Column('cummulativeQuoteQty', db.Float),
            db.Column('status', db.String(6)),
            db.Column('timeInForce', db.String(12)),
            db.Column('type', db.String(8)),
            db.Column('side', db.String(8)),
            db.Column('sellID', db.Integer),
            db.Column('trailingProfit', db.Integer),
            db.Column('kind', db.String(8)),
            )

def init():
    metadata.create_all(engine)

def insert_buy(data, kind):
    buy = Buys()
    buy.trade_id = data['trade_id']
    buy.symbol = data['symbol']
    buy.orderid = data['orderid']
    buy.orderListId = data['orderListId']
    buy.clientOrderId = data['clientOrderId']
    buy.transactTime = data['transactTime']
    buy.price = data['price']
    buy.origQty = data['origQty']
    buy.executedQty = data['executedQty']
    buy.cummulativeQuoteQty = data['cummulativeQuoteQty']
    buy.status = data['status']
    buy.timeInForce = data['timeInForce']
    buy.type = data['type']
    buy.side = data['side']
    buy.sellID = data['sellID']
    buy.trailingProfit = data['trailingProfit']
    buy.kind = kind
    buy.insert(engine)

def search_new_buys():
    #Search Trades there status is New
    query = db.select([Buys]).where(Buys.status == 'New')
    results = engine.execute(query)
    return results

def get_trade_protectionBuys():
    protectiontime = (int(time.time()) - 3300)*1000
    query = db.select([Buys]).where(Buys.transacttime > protectiontime)
    results = engine.execute(query)
    return results # TODO testing this
