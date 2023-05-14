import multiprocessing
import os
import time
import warnings
import logging

import helper.functions
import numpy as np
import pandas as pd

from multiprocessing import cpu_count

import helper.binance
import helper.config
import helper.predict


logger = helper.functions.initlogger("prediction.log")

warnings.filterwarnings('ignore')

conf = helper.config.initconfig()

if __name__ == "__main__":

    ## Create Data Folder
    if not os.path.exists('./KI'):
        os.makedirs('./KI')

    if not os.path.exists('./KI/Data'):
        os.makedirs('./KI/Data')

    if not os.path.exists('./KI/Predict'):
        os.makedirs('./KI/Predict')

    ## Search Pairs
    print("Search Pairs")

    CurrencyPairList = helper.predict.pairs()

    # CurrencyPairList = ["BTCBUSD"] #TODO overwrite the List von Exchange



    ## Request Data
    print("Request Data")

    # TODO
    helper.predict.request_all(CurrencyPairList)



    for CurrencyPair in CurrencyPairList:
        print("Prepair Data")
        X_train, y_train, X_test, y_test = helper.predict.prepair(CurrencyPair)

        # TODO
        model = helper.predict.model(X_train)

        # TODO
        helper.predict.train(model, X_train, y_train, X_test, y_test)

        helper.predict.predict(CurrencyPair, X_test, y_test, X_train)
