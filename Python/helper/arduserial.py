# Importing Libraries
import serial
import time
import requests
import helper.config
import logging
import os

conf = helper.config.initconfig()

arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=.1)

def read():
    arduino.write('1'.encode())
    # serialdata = arduino.readline()
    serialdata = arduino.read_all()
    data = {}
    data['tank_temp'] = 0
    data['line1_temp'] = 0
    data['line2_temp'] = 0
    data['durchfluss1'] = 0
    data['durchfluss2'] = 0
    if serialdata != b'':
        data['tank_temp'] = serialdata.decode().split("T1:")[1].split("\r")[0]
        data['line1_temp'] = serialdata.decode().split("T2:")[1].split("\r")[0]
        data['line2_temp'] = serialdata.decode().split("T3:")[1].split("\r")[0]
        data['durchfluss1'] = serialdata.decode().split("D1:")[1].split("\r")[0]
        data['durchfluss1'] = serialdata.decode().split("D2:")[1].split("\r")[0]
        print(serialdata.decode().strip())
    print(data)
    if (float(data['tank_temp']) > 0 and #and float(data['line1_temp']) > 0 #TODO when sensor is fixed
        float(data['line2_temp']) > 0):
        request(data)

def request(data):
    try:
        res = requests.post('http://' + conf['API_HOST'] + ':5000/api/arduino/' + os.uname().nodename, json=data, timeout=5)
        if res.ok:
            print(res.json())
    except Exception as e:
        logging.error("Fehler beim schreiben von Arduino Daten in API: " + str(e))
        print("Fehler beim schreiben von Arduino Daten in API: " + str(e))
