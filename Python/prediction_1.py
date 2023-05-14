import requests
import json
import pandas as pd

def collectingLatestBTC(timePeriod="5y"):
    r = requests.get("https://api.coinranking.com/v2/coin/Qwsogvtv82FCd/history?timePeriod=" + timePeriod)
    latest_coin = json.loads(r.text)["data"]["history"]  # Reading the JSON and cleaning the irrelevant parts
    df = pd.DataFrame(latest_coin) #Creating the dataframe
    print(df.head(10))  # uncomment this line to see the old 10 days data
    print(df.tail(10)) # uncomment this line to see the latest data of past 10 days.
    df['price'] = pd.to_numeric(df['price'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s').dt.date
    return df.groupby('timestamp').mean()['price']

if __name__ == '__main__':
    collectingLatestBTC()


# https://iotdesignpro.com/projects/implementing-deep-learning-neural-network-model-to-predict-bitcoin-price-using-tensorflow-and-keras