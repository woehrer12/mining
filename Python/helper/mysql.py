from datetime import datetime
import logging
import time

import helper.config
import mysql.connector

conf = helper.config.initconfig()


def init():
    mydb = mysql.connector.connect(
        host = conf['MYSQL_HOST'],
        user = conf['MYSQL_USER'],
        password = conf['MYSQL_PASS'],
    )
    mycursor = mydb.cursor()

    mycursor.execute("CREATE DATABASE IF NOT EXISTS Mining")
    
    mycursor.close()

    mydb = mysql.connector.connect(
    host = conf['MYSQL_HOST'],
    user = conf['MYSQL_USER'],
    password = conf['MYSQL_PASS'],
    database = 'Mining'
    )
    mycursor = mydb.cursor()
    
    # Groove
    mycursor.execute('''CREATE TABLE IF NOT EXISTS groove
                    (name text,
                    case_temp real, case_humi real, timestamp integer)''')
    
    # Arduino
    mycursor.execute('''CREATE TABLE IF NOT EXISTS arduino
                    (name text,
                    tank_temp real, line1_temp real, line2_temp real, durchfluss1 real, durchfluss2 real, timestamp integer)''')
    
    mycursor.close()

# Request
def requestsolarpower():
    try:
        mydb = mysql.connector.connect(
        host = conf['MYSQL_HOST'],
        user = conf['MYSQL_USER'],
        password = conf['MYSQL_PASS'],
        database = 'iobrokerwinzerhausen'
        )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT val FROM ts_number WHERE id = 10 ORDER BY ts DESC LIMIT 10")
        myresult = mycursor.fetchall()
        mycursor.close()

        return myresult
    except Exception as e:
        logging.error("Fehler beim lesen von solarpower Daten aus SQL: " + str(e))
        print("Fehler beim lesen von solarpower Daten aus SQL: " + str(e))


def insertgroove(data):
    try:
        mydb = mysql.connector.connect(
        host = conf['MYSQL_HOST'],
        user = conf['MYSQL_USER'],
        password = conf['MYSQL_PASS'],
        database = 'Mining'
        )
        mycursor = mydb.cursor()
        execute = """INSERT INTO groove (name, case_temp, case_humi, timestamp) VALUES (%s,%s,%s,%s)"""
        query = data['name'], data['case_temp'], data['case_humi'], time.time()
        mycursor.execute(execute, query)
        mydb.commit()
        mycursor.close()
    except Exception as e:
        logging.error("Fehler beim schreiben von Grove in SQL: " + str(e))
        print("Fehler beim schreiben von Grove in SQL: " + str(e))

def insertarduino(data):
    try:
        mydb = mysql.connector.connect(
        host = conf['MYSQL_HOST'],
        user = conf['MYSQL_USER'],
        password = conf['MYSQL_PASS'],
        database = 'Mining'
        )
        mycursor = mydb.cursor()
        execute = """INSERT INTO arduino (name, tank_temp, line1_temp, line2_temp, durchfluss1, durchfluss2, timestamp) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
        query = data['name'], data['tank_temp'], data['line1_temp'], data['line2_temp'], data['durchfluss1'], data['durchfluss2'], time.time()
        mycursor.execute(execute, query)
        mydb.commit()
        mycursor.close()
    except Exception as e:
        logging.error("Fehler beim schreiben von Arduino in SQL: " + str(e))
        print("Fehler beim schreiben von Arduino in SQL: " + str(e))
