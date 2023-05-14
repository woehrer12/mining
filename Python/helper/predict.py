import csv
import logging
import os
import time
import multiprocessing
import matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from tensorflow import keras
import tensorflow as tf

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import Bidirectional, Dropout, Activation, Dense, LSTM
from tensorflow.python.keras.layers import CuDNNLSTM
from tensorflow.keras.models import load_model, Sequential
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.metrics import mean_absolute_error, r2_score


import helper.binance

SEQ_LEN = 100
DROPOUT = 0.2
WINDOW_SIZE = SEQ_LEN - 1

scaler = MinMaxScaler()



def pairs():
    CurrencyPairList = []

    pairs = helper.binance.get_exchange_info()

    for pair in pairs['symbols']:
        if 'USDT' in pair['symbol']:
            if 'SPOT' in pair['permissions']:
                if pair['status'] == 'TRADING':
                    if pair['symbol'].endswith("USDT"):
                        CurrencyPairList.append(pair['symbol'])
    return CurrencyPairList

def request_all(CurrencyPairList):

    p = multiprocessing.Pool(4)

    for CurrencyPair in CurrencyPairList:

        p.apply_async(helper.predict.request, args=(CurrencyPair,))
        time.sleep(10)
    p.close()
    p.join()

def request(CurrencyPair):

    while True:
        try:
            logging.info("Request Data " + CurrencyPair)
            print("Request Data " + CurrencyPair)

            data = helper.binance.get_historical_klines_15m(CurrencyPair)

            # Start to Save Data
            # Open time / Open / High / Low / Close / Volume / Close time / Quote asset volume / Number of trades / Taker buy base asset volume / Taker buy quote asset volume / Ignore
            print("Save Data " + CurrencyPair)
            logging.info("Save Data " + CurrencyPair)
            if not os.path.exists('./KI/Data/CurrencyPair_{}'.format(CurrencyPair)):
                os.makedirs('./KI/Data/CurrencyPair_{}'.format(CurrencyPair))

            with open('./KI/Data/CurrencyPair_{}/Data.csv'.format(CurrencyPair), 'w', newline = '') as f:
                writer = csv.writer(f)
                writer.writerow(['Open time', 'open', 'high', 'low', 'close', 'volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
                for line in data:
                    writer.writerow(line)
            print("Finish Saved " + CurrencyPair)
            logging.info("Finish Saved " + CurrencyPair)
            break
        except Exception as e:
            logging.error("Error while request " + CurrencyPair + ": " + str(e))
            print("Error while request " + CurrencyPair + ": " + str(e))
            time.sleep(120)

def prepair(CurrencyPair):
    print("Prepair Data " + CurrencyPair)
    logging.info("Prepair Data " + CurrencyPair)
    try:
        df = pd.read_csv('./KI/Data/CurrencyPair_{}/Data.csv'.format(CurrencyPair))
        df["Date"] = pd.to_datetime(df["Open time"], unit='ms')
        df = df.sort_values('Date')
        
        ax = df.plot(x='Date', y='close')
        ax.set_xlabel("Date")
        ax.set_ylabel("Close Price (USDT)")
        fig = ax.get_figure()
        fig.savefig('./KI/Data/CurrencyPair_{}/Close.png'.format(CurrencyPair))

        # scaler = MinMaxScaler()

        close_price = df.close.values.reshape(-1, 1)

        scaled_close = scaler.fit_transform(close_price)

        scaled_close = scaled_close[~np.isnan(scaled_close)]

        scaled_close = scaled_close.reshape(-1, 1)

        def to_sequences(data, seq_len):
            d = []

            for index in range(len(data) - seq_len):
                d.append(data[index: index + seq_len])

            return np.array(d)

        def preprocess(data_raw, seq_len, train_split):

            data = to_sequences(data_raw, seq_len)

            num_train = int(train_split * data.shape[0])

            X_train = data[:num_train, :-1, :]
            y_train = data[:num_train, -1, :]

            X_test = data[num_train:, :-1, :]
            y_test = data[num_train:, -1, :]

            return X_train, y_train, X_test, y_test


        X_train, y_train, X_test, y_test = preprocess(scaled_close, SEQ_LEN, train_split = 0.95)

        return X_train, y_train, X_test, y_test



    except Exception as e:
        logging.error("Error while prepair " + CurrencyPair + ": " + str(e))
        print("Error while prepair " + CurrencyPair + ": " + str(e))

def model(X_train):
    try:
        if os.path.isdir('./KI/Models/model'):
            model = load_model('./KI/Models/model')

            print("Model loaded")
            logging.info("Model loaded")
        else:
            model = keras.Sequential()

            model.add(Bidirectional(tf.keras.layers.LSTM(WINDOW_SIZE, return_sequences=True),
                                    input_shape=(WINDOW_SIZE, X_train.shape[-1])))
            model.add(Dropout(rate=DROPOUT))

            model.add(Bidirectional(tf.keras.layers.LSTM((WINDOW_SIZE * 2), return_sequences=True)))
            model.add(Dropout(rate=DROPOUT))

            model.add(Bidirectional(tf.keras.layers.LSTM(WINDOW_SIZE, return_sequences=False)))

            model.add(Dense(units=1))

            model.add(Activation('linear'))
            model.summary()

            print("New model created")
            logging.info("New model created")
        return model

    except Exception as e:
        logging.error("Error while prepair: " + str(e))
        print("Error while prepair: " + str(e))

def train(model, X_train, y_train, X_test, y_test):
    try:
        model.compile(loss='mean_squared_error', optimizer='adam')
        BATCH_SIZE = 64

        # Define early stopping callback
        early_stop = EarlyStopping(monitor='val_loss', patience=5)


        history = model.fit(
            X_train, 
            y_train, 
            epochs=50, 
            batch_size=BATCH_SIZE, 
            shuffle=False,
            validation_split=0.1,
            callbacks=[early_stop]
        )

        model.evaluate(X_test, y_test)

        model.save('./KI/Models/model')
        print("Model trained")
        logging.info("Model trained")

        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.savefig('./KI/Models/Model_loss.png')

    except Exception as e:
            logging.error("Error while train: " + str(e))
            print("Error while train: " + str(e))

def predict(CurrencyPair, X_test, y_test, X_train):
    try:
        print("Predict Data ")
        logging.info("Predict Data ")

        # df = pd.read_csv('./KI/Data/CurrencyPair_{}/Data.csv'.format(CurrencyPair))
        # df["Date"] = pd.to_datetime(df["Open time"], unit='ms')
        # df = df.sort_values('Date')


        # scaler = MinMaxScaler()

        # close_price = df.close.values.reshape(-1, 1)

        # scaled_close = scaler.fit_transform(close_price)

        # scaled_close = scaled_close[~np.isnan(scaled_close)]

        # scaled_close = scaled_close.reshape(-1, 1)


        # Load the trained model
        model = load_model('./KI/Models/model')

        # Predict on test data
        y_hat = model.predict(X_test)

        # print(y_hat)
        # print(X_test)

        # Reshape arrays to 2 dimensions
        # y_test = np.reshape(y_test, (-1, 1))
        # y_hat = np.reshape(y_hat, (-1, 1))

        # Inverse transform test data
        print("Inverse transform")
        y_test_inverse = scaler.inverse_transform(y_test)
        y_hat_inverse = scaler.inverse_transform(y_hat)

        # Compute mean absolute error
        print("Mean absolute error")
        mae = mean_absolute_error(y_test_inverse, y_hat_inverse)

        # Compute R2 score
        print("R2 score")
        r2 = r2_score(y_test_inverse, y_hat_inverse)

        print("Mean absolute error:", mae)
        print("R2 score:", r2)

        # Reshape arrays to 1 dimension
        y_test_inverse = y_test_inverse.ravel()
        y_hat_inverse = y_hat_inverse.ravel()

        plt.clf()
        plt.plot(y_test_inverse, label="Actual Price", color='green')
        plt.plot(y_hat_inverse, label="Predicted Price", color='red')
        plt.text(0.05, 0.95, "MAE: " + str(mae) + "R2: " + str(r2), transform=plt.gca().transAxes)
        plt.title('Bitcoin price prediction')
        plt.xlabel('Time [15mins]')
        plt.ylabel('Price')
        plt.legend(loc='best')
        
        plt.savefig('./KI/Data/CurrencyPair_{}/Predict.png'.format(CurrencyPair))

    except Exception as e:
            logging.error("Error while predict: " + str(e))
            print("Error while predict: " + str(e))


def only_prepair(CurrencyPair):
    print("Only Prepair Data " + CurrencyPair)
    logging.info("Only Prepair Data " + CurrencyPair)
    try:
        df = pd.read_csv('./KI/Data/CurrencyPair_{}/Data.csv'.format(CurrencyPair))
        df["Date"] = pd.to_datetime(df["Open time"], unit='ms')
        df = df.sort_values('Date')
        
        ax = df.plot(x='Date', y='close')
        ax.set_xlabel("Date")
        ax.set_ylabel("Close Price (USDT)")
        fig = ax.get_figure()
        fig.savefig('./KI/Predict/CurrencyPair_{}/Close.png'.format(CurrencyPair))

        scaler = MinMaxScaler()

        close_price = df.close.values.reshape(-1, 1)

        scaled_close = scaler.fit_transform(close_price)

        scaled_close = scaled_close[~np.isnan(scaled_close)]

        scaled_close = scaled_close.reshape(-1, 1)

        def to_sequences(data, seq_len):
            d = []

            for index in range(len(data) - seq_len):
                d.append(data[index: index + seq_len])

            return np.array(d)

        def preprocess(data_raw, seq_len):

            data = to_sequences(data_raw, seq_len)

            X_test = data[:, :-1, :]
            y_test = data[:, -1, :]

            return X_test, y_test


        X_test, y_test = preprocess(scaled_close, SEQ_LEN)

        return X_test, y_test



    except Exception as e:
        logging.error("Error while prepair " + CurrencyPair + ": " + str(e))
        print("Error while prepair " + CurrencyPair + ": " + str(e))


def only_predict(X_test):
    try:
        print("Only Predict Data ")
        logging.info("Only Predict Data ")

        model = load_model('./KI/Models/model')

        y_hat = model.predict(X_test)

        scaler = MinMaxScaler()

        y_hat_inverse = scaler.inverse_transform(y_hat)
        
        plt.plot(y_hat_inverse, label="Predicted Price", color='red')
        
        plt.title('Bitcoin price prediction')
        plt.xlabel('Time [15mins]')
        plt.ylabel('Price')
        plt.legend(loc='best')
        
        plt.savefig('./KI/Predict/CurrencyPair_{}/Predict.png')




    except Exception as e:
        logging.error("Error while predict: " + str(e))
        print("Error while predict: " + str(e))


# https://colab.research.google.com/drive/1wWvtA5RC6-is6J8W86wzK52Knr3N1Xbm#scrollTo=4XyoR5lG3Jxv