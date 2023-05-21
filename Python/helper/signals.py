import pandas as pd
import numpy as np

import talib.abstract as ta

def prepair(df):

    # Convert the UNIX time into the date
    df["Date"] = pd.to_datetime(df["Open time"], unit='ms')

    # Sort data by date
    df = df.sort_values(by = 'Date')


    df['close'] = pd.to_numeric(df['close'])
    df['open'] = pd.to_numeric(df['open'])
    df['volume'] = pd.to_numeric(df['volume'])
    df['Bodysize'] = df['close'] - df['open']
    df['high'] = pd.to_numeric(df['high'])
    df['low'] = pd.to_numeric(df['low'])
    df['Shadowsize'] = df['high'] - df['low']

    # RSI
    df["rsi_3"] = ta.RSI(df, timeperiod=3)
    df["rsi_5"] = ta.RSI(df, timeperiod=5)
    df["rsi_6"] = ta.RSI(df, timeperiod=6)
    df["rsi_10"] = ta.RSI(df, timeperiod=10)
    df["rsi_12"] = ta.RSI(df, timeperiod=12)
    df["rsi_21"] = ta.RSI(df, timeperiod=21)
    df["rsi_24"] = ta.RSI(df, timeperiod=24)
    df["rsi_50"] = ta.RSI(df, timeperiod=50)
    df["rsi_100"] = ta.RSI(df, timeperiod=100)
    df["rsi_200"] = ta.RSI(df, timeperiod=200)

    # SMA - Simple Moving Average
    df['sma_3'] = ta.SMA(df, timeperiod=3)
    df['sma_5'] = ta.SMA(df, timeperiod=5)
    df['sma_6'] = ta.SMA(df, timeperiod=6)
    df['sma_10'] = ta.SMA(df, timeperiod=10)
    df['sma_12'] = ta.SMA(df, timeperiod=12)
    df['sma_21'] = ta.SMA(df, timeperiod=21)
    df['sma_24'] = ta.SMA(df, timeperiod=24)
    df['sma_50'] = ta.SMA(df, timeperiod=50)
    df['sma_100'] = ta.SMA(df, timeperiod=100)
    df["sma_200"] = ta.SMA(df, timeperiod=200)


    # Add modulo 10, 100, 1000, 500, 50
    df["Modulo_10"] = df["close"].copy() % 10
    df["Modulo_100"] = df["close"].copy() % 100
    df["Modulo_1000"] = df["close"].copy() % 1000
    df["Modulo_500"] = df["close"].copy() % 500
    df["Modulo_50"] = df["close"].copy() % 50

    # Add weekday and day of the month
    df["WeekDay"] = df["Date"].dt.weekday
    df["Day"] = df["Date"].dt.day


    # EMA - Exponential Moving Average
    df['ema_3'] = ta.EMA(df, timeperiod=3)
    df['ema_5'] = ta.EMA(df, timeperiod=5)
    df['ema_10'] = ta.EMA(df, timeperiod=10)
    df['ema_21'] = ta.EMA(df, timeperiod=21)
    df['ema_50'] = ta.EMA(df, timeperiod=50)
    df['ema_100'] = ta.EMA(df, timeperiod=100)

    hilbert = ta.HT_SINE(df)
    df['htsine'] = hilbert['sine']
    df['htleadsine'] = hilbert['leadsine']

    # TODO Add more indicators
    df['adx'] = ta.ADX(df)
    df['adxr'] = ta.ADXR(df)
    df['apo'] = ta.APO(df)
    aroon = ta.AROON(df)
    df['aroonup'] = aroon['aroonup']
    df['aroondown'] = aroon['aroondown']
    df['aroonosc'] = ta.AROONOSC(df)
    df['bop'] = ta.BOP(df)
    df['cci'] = ta.CCI(df)
    df['cmo'] = ta.CMO(df)
    df['dx'] = ta.DX(df)
    macd = ta.MACD(df)
    df['macd'] = macd['macd']
    df['macdsignal'] = macd['macdsignal']
    df['macdhist'] = macd['macdhist']
    df['mfi'] = ta.MFI(df)
    df['minus_di'] = ta.MINUS_DI(df)
    df['minus_dm'] = ta.MINUS_DM(df)
    df['mom'] = ta.MOM(df)
    df['plus_di'] = ta.PLUS_DI(df)
    df['plus_dm'] = ta.PLUS_DM(df)
    df['ppo'] = ta.PPO(df)
    df['roc'] = ta.ROC(df)
    df['rocp'] = ta.ROCP(df)
    df['rocr'] = ta.ROCR(df)
    df['rocr100'] = ta.ROCR100(df)
    df['rsi'] = ta.RSI(df)
    rsi = 0.1 * (df['rsi'] - 50)
    df['fisher_rsi'] = (np.exp(2 * rsi) - 1) / (np.exp(2 * rsi) + 1)
    df['fisher_rsi_norma'] = 50 * (df['fisher_rsi'] + 1)
    stoch = ta.STOCH(df)
    df['slowd'] = stoch['slowd']
    df['slowk'] = stoch['slowk']
    stoch_fast = ta.STOCHF(df)
    df['fastd'] = stoch_fast['fastd']
    df['fastk'] = stoch_fast['fastk']
    stoch_rsi = ta.STOCHRSI(df)
    df['fastd_rsi'] = stoch_rsi['fastd']
    df['fastk_rsi'] = stoch_rsi['fastk']
    df['sar'] = ta.SAR(df)
    df['tema'] = ta.TEMA(df, timeperiod=9)
    df['trix'] = ta.TRIX(df)
    df['ultosc'] = ta.ULTOSC(df)
    df['willr'] = ta.WILLR(df)

    # Pattern Recognition - Bullish candlestick patterns
    # ------------------------------------
    # Hammer: values [0, 100]
    df['CDLHAMMER'] = ta.CDLHAMMER(df)
    # Inverted Hammer: values [0, 100]
    df['CDLINVERTEDHAMMER'] = ta.CDLINVERTEDHAMMER(df)
    # Dragonfly Doji: values [0, 100]
    df['CDLDRAGONFLYDOJI'] = ta.CDLDRAGONFLYDOJI(df)
    # Piercing Line: values [0, 100]
    df['CDLPIERCING'] = ta.CDLPIERCING(df) # values [0, 100]
    # Morningstar: values [0, 100]
    df['CDLMORNINGSTAR'] = ta.CDLMORNINGSTAR(df) # values [0, 100]
    # Three White Soldiers: values [0, 100]
    df['CDL3WHITESOLDIERS'] = ta.CDL3WHITESOLDIERS(df) # values [0, 100]

    # Pattern Recognition - Bearish candlestick patterns
    # ------------------------------------
    # Hanging Man: values [0, 100]
    df['CDLHANGINGMAN'] = ta.CDLHANGINGMAN(df)
    # Shooting Star: values [0, 100]
    df['CDLSHOOTINGSTAR'] = ta.CDLSHOOTINGSTAR(df)
    # Gravestone Doji: values [0, 100]
    df['CDLGRAVESTONEDOJI'] = ta.CDLGRAVESTONEDOJI(df)
    # Dark Cloud Cover: values [0, 100]
    df['CDLDARKCLOUDCOVER'] = ta.CDLDARKCLOUDCOVER(df)
    # Evening Doji Star: values [0, 100]
    df['CDLEVENINGDOJISTAR'] = ta.CDLEVENINGDOJISTAR(df)
    # Evening Star: values [0, 100]
    df['CDLEVENINGSTAR'] = ta.CDLEVENINGSTAR(df)

    # Pattern Recognition - Bullish/Bearish candlestick patterns
    # ------------------------------------
    # Three Line Strike: values [0, -100, 100]
    df['CDL3LINESTRIKE'] = ta.CDL3LINESTRIKE(df)
    # Spinning Top: values [0, -100, 100]
    df['CDLSPINNINGTOP'] = ta.CDLSPINNINGTOP(df) # values [0, -100, 100]
    # Engulfing: values [0, -100, 100]
    df['CDLENGULFING'] = ta.CDLENGULFING(df) # values [0, -100, 100]
    # Harami: values [0, -100, 100]
    df['CDLHARAMI'] = ta.CDLHARAMI(df) # values [0, -100, 100]
    # Three Outside Up/Down: values [0, -100, 100]
    df['CDL3OUTSIDE'] = ta.CDL3OUTSIDE(df) # values [0, -100, 100]
    # Three Inside Up/Down: values [0, -100, 100]
    df['CDL3INSIDE'] = ta.CDL3INSIDE(df) # values [0, -100, 100]

    df["RSI"] = ta.RSI(df["close"], timeperiod = 14)
    df["ROC"] = ta.ROC(df["close"], timeperiod = 10)
    df["%R"] = ta.WILLR(df["high"], df["low"], df["close"], timeperiod = 14)
    df["OBV"] = ta.OBV(df["close"], df["volume"])
    df["MACD"], df["MACD_SIGNAL"], df["MACD_HIST"] = ta.MACD(df["close"], fastperiod=12, slowperiod=26, signalperiod=9)

    period = 20
    std_dev = 2

    rolling_mean = df['close'].rolling(window=period).mean()
    rolling_std = df['close'].rolling(window=period).std()

    df['bb_lowerband'] = rolling_mean - (rolling_std * std_dev)
    df['bb_middleband'] = rolling_mean
    df['bb_upperband'] = rolling_mean + (rolling_std * std_dev)
    
    df["Prediction"] = np.where(df["close"].shift(-5) > df["close"], 1, -1)


    return df

def prepair_data(data):

    df = pd.DataFrame(  data,
                        columns =['Open time', 'open', 'high', 'low', 'close', 'volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])

    df = prepair(df)

    return df

def multi_prepair(CurrencyPair):
    df = pd.read_csv('./Data/CurrencyPair_{}/Data.csv'.format(CurrencyPair))

    # Sort Data
    print("Sort Data " + CurrencyPair)
    df = prepair(df)

    df.to_csv('./Data/CurrencyPair_{}/Sorted.csv'.format(CurrencyPair), index=False)
