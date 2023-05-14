import os
import requests
import helper.config
import logging
import time
import seeed_dht

conf = helper.config.initconfig()

def check():
    data = {}
    sensor = seeed_dht.DHT("11", 16)
    data['case_humi'], data['case_temp'] = sensor.read()
    print("Case Temp: " + str(data['case_temp']) + "°C")
    print("Case Humi: " + str(data['case_humi']) + "%")
    if data['case_humi'] > 0 and data['case_temp'] > 0:
        request(data)

def request(data):
    try:
        res = requests.post('http://' + conf['API_HOST'] + ':5000/api/groove/' + os.uname().nodename, json=data, timeout=5)
        if res.ok:
            print(res.json())
    except Exception as e:
        logging.error("Fehler beim schreiben von groove Daten in API: " + str(e))
        print("Fehler beim schreiben von groove Daten in API: " + str(e))
