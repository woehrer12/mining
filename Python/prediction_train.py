import csv
import logging
import multiprocessing
import os
import time
import warnings
from datetime import datetime

import helper.functions
import numpy as np
import pandas as pd

logger = helper.functions.initlogger("prediction.log")

from multiprocessing import cpu_count

import helper.binance
import helper.config
import helper.predict
# import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.layers import *
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.metrics import RootMeanSquaredError
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.optimizers import Adam

# from tensorflow.keras import layers
# from tensorflow.keras.callbacks import EarlyStopping
# from sklearn.model_selection import train_test_split
# import tensorflow_decision_forests as tfdf
# import keras_tuner as kt



warnings.filterwarnings('ignore')

conf = helper.config.initconfig()

CurrencyPairList = []

pairs = helper.binance.get_exchange_info()

for pair in pairs['symbols']:
    if 'USDT' in pair['symbol']:
        if 'SPOT' in pair['permissions']:
            if pair['status'] == 'TRADING':
                if pair['symbol'].endswith("USDT"):
                    CurrencyPairList.append(pair['symbol'])
print(CurrencyPairList)
print(len(CurrencyPairList))


# CurrencyPairList = ["BTCBUSD","ETHBUSD","BNBBUSD","XMRBUSD","ATOMBUSD","LUNCBUSD","ADABUSD","AMBBUSD","XRPBUSD","SOLBUSD","DOGEBUSD","DOTBUSD","MATICBUSD","ERNBUSD","SHIBBUSD","SUNBUSD","LUNABUSD"]
CurrencyPairList = ["BTCBUSD"] #TODO overwrite the List von Exchange


if conf['train'] == 'True':

    if os.path.isdir('./KI/Models/model'):
        model1 = load_model('./KI/Models/model')

        print("Model loaded")
        logging.info("Model loaded")
    else:
        model1 = Sequential()
        model1.add(InputLayer((500, 1)))
        model1.add(LSTM(64))
        model1.add(Dense(8, 'relu'))
        model1.add(Dense(1, 'linear'))

        model1.summary()

        print("New model created")
        logging.info("New model created")

    for CurrencyPair in CurrencyPairList:

        df = pd.read_csv('./KI/Data/CurrencyPair_{}/Sorted.csv'.format(CurrencyPair))

        print(df)

        temp = df['close']

        def df_to_X_y(df, window_size):
            df_as_np = df.to_numpy()
            X = []
            y = []
            for i in range(len(df_as_np)-window_size):
                row = [[a] for a in df_as_np[i:i+window_size]]
                X.append(row)
                label = df_as_np[i+window_size]
                y.append(label)
            return np.array(X), np.array(y)

        WINDOW_SIZE = 500
        X1, y1 = df_to_X_y(temp, WINDOW_SIZE)
        X1.shape, y1.shape

        X_train1, y_train1 = X1[:int(0.7*len(X1))], y1[:int(0.7*len(y1))]
        X_val1, y_val1 = X1[int(0.7*len(X1)):int(0.9*len(X1))], y1[int(0.7*len(y1)):int(0.9*len(y1))]
        X_test1, y_test1 = X1[int(0.9*len(X1)):], y1[int(0.9*len(y1)):]
        X_train1.shape, y_train1.shape, X_val1.shape, y_val1.shape, X_test1.shape, y_test1.shape

        cp1 = ModelCheckpoint('./KI/Models/model', save_best_only=True)
        model1.compile(loss=MeanSquaredError(), optimizer=Adam(learning_rate=0.0001), metrics=[RootMeanSquaredError()])


        model1.fit(X_train1, y_train1, validation_data=(X_val1, y_val1), epochs=10, callbacks=[cp1], workers=cpu_count())

        model1.save('./KI/Models/model')

        # Laden des Modells
        model1 = load_model('./KI/Models/model')

        # Vorhersage auf Testdaten durchführen
        y_pred = model1.predict(X_test1)

        # Ausgabe der Vorhersage und des tatsächlichen Wertes
        correct_predictions = 0
        for i in range(len(y_pred)):
            prediction = y_pred[i][0]
            actual = y_test1[i]
            if abs(prediction - actual) < 0.01:  # assume correct if prediction is within 1% of actual
                correct_predictions += 1
            print(f"Prediction: {prediction}, Actual: {actual} for {CurrencyPair}")
            logging.info(f"Prediction: {prediction}, Actual: {actual} for {CurrencyPair}")
        accuracy = 100 * correct_predictions / len(y_pred)
        print(f"Accuracy: {accuracy:.2f}%")
        logging.info(f"Accuracy: {accuracy:.2f}% for {CurrencyPair}")


if conf['predict'] == 'True':
    # Prediction Part
    model1 = load_model('./KI/Models/model/')

    data = helper.binance.get_klines(CurrencyPair)

    df = helper.training.sort_data(CurrencyPair,1)

    prediction = model1.predict(df)

    print(prediction)
