import sqlalchemy as db
import time

import helper.config

conf = helper.config.initconfig()

connection_string = "mysql+mysqlconnector://" + conf['MYSQL_USER'] + ":" + conf['MYSQL_PASS'] + "@" + conf['MYSQL_HOST'] + ":3306/sqlalchemy"

metadata = db.MetaData()

Buys = db.Table('Buys', metadata,
            db.Column('trade_id', db.Integer(),primary_key = True),
            db.Column('symbol', db.String(8), nullable = False),
            db.Column('orderid', db.BigInteger),
            db.Column('orderListId', db.Integer),
            db.Column('clientOrderId', db.String(24)),
            db.Column('transactTime', db.BigInteger),
            db.Column('sell_transactTime', db.BigInteger),
            db.Column('price', db.Float),
            db.Column('origQty', db.Float),
            db.Column('executedQty', db.Float),
            db.Column('cummulativeQuoteQty', db.Float),
            db.Column('status', db.String(6)),
            db.Column('sell_status', db.String(6)),
            db.Column('timeInForce', db.String(12)),
            db.Column('type', db.String(8)),
            db.Column('side', db.String(8)),
            db.Column('sellID', db.Integer),
            db.Column('trailingProfit', db.Integer),
            db.Column('kind', db.String(8)),
            )

def init():
    engine = db.create_engine(connection_string, connect_args={'connect_timeout': 10})
    metadata.create_all(engine)

def insert_buy(data, kind):
    engine = db.create_engine(connection_string, connect_args={'connect_timeout': 10})
    conn = engine.connect()
    query = db.insert(Buys).values(symbol = data['symbol'],
                                   orderid = data['orderId'],
                                   orderListId = data['orderListId'],
                                   clientOrderId = data['clientOrderId'],
                                   transactTime = data['transactTime'],
                                   price = data['price'],
                                   origQty = data['origQty'],
                                   executedQty = data['executedQty'],
                                   cummulativeQuoteQty = data['cummulativeQuoteQty'],
                                   status = data['status'],
                                   timeInForce = data['timeInForce'],
                                   type = data['type'],
                                   side = data['side'],
                                   kind = kind
                                   )

    # Beginne eine Transaktion
    trans = conn.begin()

    try:
        conn.execute(query)

        # Bestätige die Transaktion
        trans.commit()
    except:
        # Bei einem Fehler mache einen Rollback der Transaktion
        trans.rollback()
        raise
    finally:
        conn.close()

def search_id(id):
    #Search Trades there id is ??
    engine = db.create_engine(connection_string, connect_args={'connect_timeout': 10})
    conn = engine.connect()
    query = db.select(Buys).where(Buys.c.trade_id == id)
    results = conn.execute(query)
    conn.close()
    return results

def search_id(id):
    #Search Trades there id is ??
    engine = db.create_engine(connection_string, connect_args={'connect_timeout': 10})
    conn = engine.connect()
    query = db.select(Buys).where(Buys.c.trade_id == id)
    results = conn.execute(query)
    conn.close()
    return results

def search_new_buys():
    #Search Trades there status is New
    engine = db.create_engine(connection_string, connect_args={'connect_timeout': 10})
    conn = engine.connect()
    query = db.select(Buys).where(Buys.c.status == 'NEW')
    results = conn.execute(query)
    conn.close()
    return results

def search_new_sells():
    #Search Trades there status is New
    engine = db.create_engine(connection_string, connect_args={'connect_timeout': 10})
    conn = engine.connect()
    query = db.select(Buys).where(Buys.c.sell_status == 'NEW')
    results = conn.execute(query)
    conn.close()
    return results

def search_filled_buys():
    #Search Trades there status is Filled
    engine = db.create_engine(connection_string, connect_args={'connect_timeout': 10})
    conn = engine.connect()
    query = db.select(Buys).where((Buys.c.status == 'Filled') & (Buys.c.sellID == ''))
    results = conn.execute(query)
    conn.close()
    return results

def get_trade_protectionBuys():
    engine = db.create_engine(connection_string, connect_args={'connect_timeout': 10})
    conn = engine.connect()
    protectiontime = (int(time.time()) - 3300)*1000
    query = db.select(Buys).where(Buys.c.transactTime > protectiontime)
    results = conn.execute(query)
    conn.close()
    if results.rowcount > 0:
        return True
    return False

def get_trade_protectionSells():
    engine = db.create_engine(connection_string, connect_args={'connect_timeout': 10})
    conn = engine.connect()
    protectiontime = (int(time.time()) - 3300)*1000
    query = db.select(Buys).where(Buys.c.sell_transactTime > protectiontime)
    results = conn.execute(query)
    conn.close()
    if results.rowcount > 0:
        return True
    return False

def update_buys(data, trade_id):
    engine = db.create_engine(connection_string, connect_args={'connect_timeout': 10})
    conn = engine.connect()
    query = db.update(Buys).where(Buys.c.trade_id == trade_id).values(
                                                                    transactTime = data['time'],
                                                                    price = data['price'],
                                                                    origQty = data['origQty'],
                                                                    executedQty = data['executedQty'],
                                                                    cummulativeQuoteQty = data['cummulativeQuoteQty'],
                                                                    status = data['status'],
                                                                    timeInForce = data['timeInForce'],
                                                                    type = data['type'],
                                                                    side = data['side']
                                                                    )
    # Beginne eine Transaktion
    trans = conn.begin()

    try:
        conn.execute(query)

        # Bestätige die Transaktion
        trans.commit()
    except:
        # Bei einem Fehler mache einen Rollback der Transaktion
        trans.rollback()
        raise
    finally:
        conn.close()
    
def update_buys_Sell_id(result, trade_id):
    engine = db.create_engine(connection_string, connect_args={'connect_timeout': 10})
    conn = engine.connect()
    query = db.update(Buys).where(Buys.c.trade_id == trade_id).values(
                                                                    sellId = result['orderId'],
                                                                    sell_tranacttime = result['transactTime'],
                                                                    sell_status = 'NEW'
                                                                    )
    # Beginne eine Transaktion
    trans = conn.begin()

    try:
        conn.execute(query)

        # Bestätige die Transaktion
        trans.commit()
    except:
        # Bei einem Fehler mache einen Rollback der Transaktion
        trans.rollback()
        raise
    finally:
        conn.close()
    
def update_buys_Sell_status(status, trade_id):
    engine = db.create_engine(connection_string, connect_args={'connect_timeout': 10})
    conn = engine.connect()
    query = db.update(Buys).where(Buys.c.trade_id == trade_id).values(
                                                                    sellId = id,
                                                                    sell_status = status
                                                                    )
    # Beginne eine Transaktion
    trans = conn.begin()

    try:
        conn.execute(query)

        # Bestätige die Transaktion
        trans.commit()
    except:
        # Bei einem Fehler mache einen Rollback der Transaktion
        trans.rollback()
        raise
    finally:
        conn.close()

def update_trailing(trailing, trade_id):
    engine = db.create_engine(connection_string, connect_args={'connect_timeout': 10})
    conn = engine.connect()
    query = db.update(Buys).where(Buys.c.trade_id == trade_id).values(
                                                                    trailingProfit = trailing,
                                                                    )
    # Beginne eine Transaktion
    trans = conn.begin()

    try:
        conn.execute(query)

        # Bestätige die Transaktion
        trans.commit()
    except:
        # Bei einem Fehler mache einen Rollback der Transaktion
        trans.rollback()
        raise
    finally:
        conn.close()

def update_trailing_to_null(trailing, trade_id):
    engine = db.create_engine(connection_string, connect_args={'connect_timeout': 10})
    conn = engine.connect()
    query = db.update(Buys).where(Buys.c.trade_id == trade_id).values(
                                                                    trailingProfit = None,
                                                                    )
    # Beginne eine Transaktion
    trans = conn.begin()

    try:
        conn.execute(query)

        # Bestätige die Transaktion
        trans.commit()
    except:
        # Bei einem Fehler mache einen Rollback der Transaktion
        trans.rollback()
        raise
    finally:
        conn.close()

def update_delete_sell(trade_id):
    engine = db.create_engine(connection_string, connect_args={'connect_timeout': 10})
    conn = engine.connect()
    query = db.update(Buys).where(Buys.c.trade_id == trade_id).values(
                                                                    sellId = None,
                                                                    sell_status = None
                                                                    )
    # Beginne eine Transaktion
    trans = conn.begin()

    try:
        conn.execute(query)

        # Bestätige die Transaktion
        trans.commit()
    except:
        # Bei einem Fehler mache einen Rollback der Transaktion
        trans.rollback()
        raise
    finally:
        conn.close()

def delete_buys(trade_id):
    engine = db.create_engine(connection_string, connect_args={'connect_timeout': 10})
    conn = engine.connect()
    query = db.delete(Buys).where(Buys.c.trade_id == trade_id)

    # Beginne eine Transaktion
    trans = conn.begin()

    try:
        conn.execute(query)

        # Bestätige die Transaktion
        trans.commit()
    except:
        # Bei einem Fehler mache einen Rollback der Transaktion
        trans.rollback()
        raise
    finally:
        conn.close()
