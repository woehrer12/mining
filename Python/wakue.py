import os
import time

import helper.arduserial
import helper.functions
import helper.groovesensor

#Inizialisierung der Konfiguration

helper.functions.initlogger("wakue.log")

def loop():
    while True:
        os.system('clear')

        helper.groovesensor.check()

        helper.arduserial.read()

        time.sleep(10)


if __name__ == "__main__":
    loop()