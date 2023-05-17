import json
import os
import shutil

def handler(data):
    if not os.path.isfile('./Python/strategies/strategie.json'):
        shutil.copyfile('./Python/strategies/strategie.json.example','./Python/strategies/strategie.json')
    data['enter_long'] = 0
    data['exit_long'] = 0
    data['strategy'] = ''

    data = RSI(data)

    data = ClucMay72018(data)

    return data



def RSI(data):
    f = open("./Python/strategies/strategie.json")
    file = json.load(f)
    
    if  (float(data['rsi_6'].iloc[-2:-1]) < file['RSI_enter']['1'] and \
        float(data['sma_6'].iloc[-2:-1]) > float(data['close'].iloc[-2:-1])) or \
        (float(data['rsi_12'].iloc[-2:-1]) < file['RSI_enter']['2'] and \
        float(data['sma_12'].iloc[-2:-1]) > float(data['close'].iloc[-2:-1])) or \
        (float(data['rsi_24'].iloc[-2:-1]) < file['RSI_enter']['3'] and \
        float(data['sma_24'].iloc[-2:-1]) > float(data['close'].iloc[-2:-1])) or \
        (float(data['rsi_200'].iloc[-2:-1]) < file['RSI_enter']['4'] and \
        float(data['sma_200'].iloc[-2:-1]) > float(data['close'].iloc[-2:-1])):
            data['enter_long'].iloc[-1] = 1
            data['strategy'] = data['strategy'] + 'RSI'
    
    if  (float(data['rsi_6'].iloc[-2:-1]) > file['RSI_exit']['1'] and \
        float(data['sma_6'].iloc[-2:-1]) < float(data['close'].iloc[-2:-1])) or \
        (float(data['rsi_12'].iloc[-2:-1]) > file['RSI_exit']['2'] and \
        float(data['sma_12'].iloc[-2:-1]) < float(data['close'].iloc[-2:-1])) or \
        (float(data['rsi_24'].iloc[-2:-1]) > file['RSI_exit']['3'] and \
        float(data['sma_24'].iloc[-2:-1]) < float(data['close'].iloc[-2:-1])) or \
        (float(data['rsi_200'].iloc[-2:-1]) > file['RSI_exit']['4'] and \
        float(data['sma_200'].iloc[-2:-1]) < float(data['close'].iloc[-2:-1])):
            data['exit_long'].iloc[-1] = 1
            data['strategy'] = data['strategy'] + 'RSI'

    return data

def ClucMay72018(data):
    f = open("./Python/strategies/strategie.json")
    file = json.load(f)

    if  (float(data['close'].iloc[-2:-1]) < float(data['ema_100'].iloc[-2:-1])) & \
        (float(data['close'].iloc[-2:-1]) < 0.985 * float(data['bb_lowerband'].iloc[-2:-1])) & \
        (float(data['volume'].iloc[-2:-1]) < (float(data['volume'].rolling(window=30).mean().shift(1).iloc[-2:-1]) * 20.0)):
            data['enter_long'].iloc[-1] = 1
            data['strategy'] = data['strategy'] + 'ClucMay72018'


    if  (float(data['close'].iloc[-2:-1]) > (float(data['bb_middleband'].iloc[-2:-1]))*1.2):
            data['exit_long'].iloc[-1] = 1
            data['strategy'] = data['strategy'] + 'ClucMay72018'

    return data