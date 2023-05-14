import requests
import datetime
import time
import json
import hmac

import helper.config

import uuid, hmac, hashlib, requests, json, base64

conf = helper.config.initconfig()

# https://www.nicehash.com/docs/rest/get-main-api-v2-mining-algo-stats

# GET https://api2.nicehash.com/main/api/v2/mining/rigs

def farms():
    url = 'https://api.hiveos.farm/api/v2/farms'

    api_token = conf['hiveosAPI']

    headers = {
        'Authorization': f'Bearer {api_token}'
    }

    response = requests.get(url, headers=headers)

    if response.ok:
        data = response.json()
        print(data)
    else:
        print('Fehler:', response.status_code)

def workers():
    farm_id = conf['hiveosfarmid']

    # URL für die API-Anfrage zum Stoppen des Miners
    url = 'https://api.hiveos.farm/api/v2/farms/' + str(farm_id) + '/workers'

    # API-Token
    api_token = conf['hiveosAPI']

    # Header mit dem API-Token
    headers = {
        'Authorization': f'Bearer {api_token}'
    }

    # Anfrage senden und Response erhalten
    response = requests.get(url, headers=headers)

    # Response auf Inhalt prüfen
    if response.ok:
        data = response.json()
        print(data)
    else:
        print('Fehler:', response.status_code)


def worker():

    farm_id = conf['hiveosfarmid']
    worker_id = conf['hiveosworkerid']

    # URL für die API-Anfrage zum Stoppen des Miners
    url = 'https://api.hiveos.farm/api/v2/farms/' + farm_id + '/workers/' + worker_id

    # API-Token
    api_token = conf['hiveosAPI']

    # Header mit dem API-Token
    headers = {
        'Authorization': f'Bearer {api_token}'
    }

    # Anfrage senden und Response erhalten
    response = requests.get(url, headers=headers)

    # Response auf Inhalt prüfen
    if response.ok:
        data = response.json()
        print(data)
    else:
        print('Fehler:', response.status_code)

def changefs(payload):

    farm_id = conf['hiveosfarmid']
    worker_id = conf['hiveosworkerid']

    # URL für die API-Anfrage zum Stoppen des Miners
    url = 'https://api.hiveos.farm/api/v2/farms/' + farm_id + '/workers/' + worker_id #+ '/command'

    print(url)

    # API-Token
    api_token = conf['hiveosAPI']

    # Header mit dem API-Token
    headers = {
        'Authorization': f'Bearer {api_token}'
    }

    # Anfrage senden und Response erhalten
    response = requests.patch(url, headers=headers, json=payload)

    # Response auf Inhalt prüfen
    if response.ok:
        data = response.json()
        print(data)
    else:
        print('Fehler:', response.status_code)

def flightsheet():

    farm_id = conf['hiveosfarmid']

    # URL für die API-Anfrage zum Stoppen des Miners
    url = 'https://api.hiveos.farm/api/v2/farms/' + farm_id + '/fs'

    print(url)

    # API-Token
    api_token = conf['hiveosAPI']

    # Header mit dem API-Token
    headers = {
        'Authorization': f'Bearer {api_token}'
    }

    # Anfrage senden und Response erhalten
    response = requests.get(url, headers=headers)

    # Response auf Inhalt prüfen
    if response.ok:
        data = response.json()
        print(data)
    else:
        print('Fehler:', response.status_code)