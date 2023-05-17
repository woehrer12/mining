import flask

import helper.functions
import helper.mysql
import helper.config

from flask import request, jsonify
logger = helper.functions.initlogger("API.log")

app = flask.Flask(__name__)

conf = helper.config.initconfig()

helper.mysql.init()

@app.route('/api/psutil/<uuid>', methods=['GET', 'POST'])
def add_message_psutil(uuid):
    data = request.json
    data['name'] = str(uuid)
    print("psutil: " + uuid)
    helper.mysql.insertpsutil(data)
    return jsonify({"uuid":uuid})

@app.route('/api/groove/<uuid>', methods=['GET', 'POST'])
def add_message_groove(uuid):
    data = request.json
    data['name'] = str(uuid)
    print("groove: " + uuid)
    helper.mysql.insertgroove(data)
    return jsonify({"uuid":uuid})

@app.route('/api/arduino/<uuid>', methods=['GET', 'POST'])
def add_message_arduino(uuid):
    data = request.json
    data['name'] = str(uuid)
    print("arduino: " + uuid)
    helper.mysql.insertarduino(data)
    return jsonify({"uuid":uuid})


if __name__ == '__main__':
    app.run(host= conf['host'],debug=False)
