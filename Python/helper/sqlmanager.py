import sqlalchemy as db

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