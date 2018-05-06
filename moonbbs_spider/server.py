#!/usr/bin/env python
# -- coding: utf-8 --
from flask import Flask, request, jsonify
import sys
from logger import moonbbs_log
import json
from repository import text_repo
from main import main_service

writer = text_repo('./wishlist.txt')

service = main_service(writer)

reload(sys)
sys.setdefaultencoding('utf8')

LOG = moonbbs_log()

app = Flask(__name__)

@app.route('/')
def index():
    return "welcome to moonbbs"

@app.route('/wish', methods=['POST'])
def add_wish():
    if (request.headers.get('Content-type') == 'application/json'):
        try:
            data = json.loads(request.data)
        except Exception as e:
            LOG.error("not json format")

            return jsonify({"errorInfo": "malformat Json"}), 403

        num = data.get('num')
        wishes = []
        if (num < 1):
            return None
        else:
            for i in range(1, num+1):
                wishes.append(data.get('items').get(str(i)))

        try:
            writer.write_wish(wishes)
        except Exception as e:
            LOG.error('failed to write in wishes')
            return jsonify({"errorInfo": "wishlist file broken"}), 404

        return jsonify({"status": "ok"}), 200
    else:
        return jsonify({"errorInfo": "json format body needed"}), 409

@app.route('/email', methods=['POST'])
def set_email():
    if (request.headers.get('Content-type') == 'application/json'):
        try:
            data = json.loads(request.data)
        except Exception as e:
            LOG.error("not json format")

            return jsonify({"errorInfo": "malformat Json"}), 403

        email = data.get('email')
        password = data.get('password')

        try:
            service.set_email(email, password)
        except Exception as e:
            LOG.error('failed to set up email')
            return jsonify({"errorInfo": "email address set up failed"}), 404

        return jsonify({"status": "ok"}), 200
    else:
        return jsonify({"errorInfo": "json format body needed"}), 409

@app.route('/interval/<int:interval>', methods=['POST'])
def set_interval(interval):
    service.set_interval(interval)
    return jsonify({"status": "ok"}), 200

@app.route('/wish', methods=['GET'])
def get_wish():
    pass

@app.route('/start', methods=['POST'])
def start():
    try:
        service.on_start()
    except Exception as e:
        LOG.error("stopped for some reason {0}".format(e))
        return jsonify({"errorInfo": "Stopped"}), 400

if __name__ == '__main__':
    app.run(host='localhost', port=80, debug=True)
