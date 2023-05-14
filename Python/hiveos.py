import helper.hiveosAPI
import helper.mysql
import helper.telegramsend
import helper.config
import time
import helper.functions
import logging

logger = helper.functions.initlogger("hiveos.log")

helper.mysql.init()

conf = helper.config.initconfig()

print("Start HiveOS")
logging.info("Start hiveos.py")

started = False

def loop():
    while True:
        # Request Solar Power
        result = helper.mysql.requestsolarpower()

        x = 0.0
        for i in result:
            if None in i:
                logging.error("None in Result")
                break
            x += float(i[0])

        avg = x / len(result)

        print(avg)

        if avg < float(conf['hiveosmaxpower']) and not started:
            helper.telegramsend.send("Start Mining")

            # Payload für RVN
            payload = {
                'fs_id': '16734657',
                }
            helper.hiveosAPI.changefs(payload)
            started = True

        if avg > float(conf['hiveosminpower']) and started:
            helper.telegramsend.send("Stop Mining")
            
            # Payload 0
            payload = {
                'fs_id': None,
                }

            helper.hiveosAPI.changefs(payload)
            started = False
        time.sleep(60)

def benchmarking():
    # Payload für ETC
    payload = {
        'fs_id': '16733974',
    }

    # Payload für RVN
    payload = {
        'fs_id': '16734657',
    }

    helper.hiveosAPI.changefs(payload)

if __name__ == "__main__":
    loop()