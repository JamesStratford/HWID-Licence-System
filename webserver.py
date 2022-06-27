from flask import Flask, send_file, request
from threading import Thread
import io
from hwiddb import Database
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask('server')

@app.route('/')
def home():
    return "Hello. I am alive!"

@app.route('/request')
def request_access():
    name = request.args.get('name')
    hwid = request.args.get('hwid')
    print("User asking for access:")
    print("    {} : {}".format(name, hwid))
    db = Database()
    db.put(name, hwid, table="REQUESTS")
    return "success"

@app.route('/access')
def access():
    hwid = request.args.get('hwid')
    db = Database()
    if db.check_hwid_exists(hwid):
        if db.check_subscription_valid(hwid):
            # Access key to be verified by loader
            return "Enter secret key here"
    return "0"
    
@app.route('/files/1/')
def file_1():
    hwid = request.args.get('hwid')
    db = Database()
    if db.check_hwid_exists(hwid):
        if db.check_subscription_valid(hwid):
            with open("files/1", 'rb') as bites:
                return send_file(
                             io.BytesIO(bites.read()),
                             attachment_filename='1',
                             mimetype='1'
                       )

@app.route('/files/2/')
def file_2():
    hwid = request.args.get('hwid')
    db = Database()
    if db.check_hwid_exists(hwid):
        if db.check_subscription_valid(hwid):
            with open("files/2", 'rb') as bites:
                return send_file(
                             io.BytesIO(bites.read()),
                             attachment_filename='2',
                             mimetype='2'
                       )

@app.route('/files/3/')
def file_3():
    hwid = request.args.get('hwid')
    db = Database()
    if db.check_hwid_exists(hwid):
        if db.check_subscription_valid(hwid):
            with open("files/3", 'rb') as bites:
                return send_file(
                             io.BytesIO(bites.read()),
                             attachment_filename='3',
                             mimetype='3'
                   )

@app.route('/files/4/')
def file_4():
    hwid = request.args.get('hwid')
    db = Database()
    if db.check_hwid_exists(hwid):
        if db.check_subscription_valid(hwid):
            with open("files/4", 'rb') as bites:
                return send_file(
                             io.BytesIO(bites.read()),
                             attachment_filename='4',
                             mimetype='4'
                   )
    
def run():
    app.run(host='0.0.0.0',port=8080)


def web_server():
    t = Thread(target=run)
    t.start()