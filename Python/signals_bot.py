import helper.binance
import helper.signals
import helper.telegramsend
import schedule
import strategies.main
import warnings
import time

warnings.filterwarnings('ignore')

listofpairs = []

pairs = helper.binance.get_exchange_info()

for pair in pairs['symbols']:
    if 'USDT' in pair['symbol']:
        if 'SPOT' in pair['permissions']:
            if pair['status'] == 'TRADING':
                listofpairs.append(pair)
print(listofpairs)



for CurrencyPair in listofpairs:
    data = helper.binance.get_klines(CurrencyPair['symbol'])

    prepaired_data = helper.signals.prepair_data(data)

    data = strategies.main.handler(prepaired_data)

    if data['enter_long'].iloc[-1] == 1:
        print('Enter: ' + str(CurrencyPair['symbol']) + ' ' + str(data['strategy'].iloc[-1]))
        #print(CurrencyPair)
    if data['exit_long'].iloc[-1] == 1:
        print('Exit: ' + str(CurrencyPair['symbol']) + ' ' + str(data['strategy'].iloc[-1]))
    #time.sleep(5)

