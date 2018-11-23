#!/usr/bin/python

# John-Michael O'Brien
# 09/24/2018
#
# A basic web service.

from flask import Flask
from flask import request
from flask import render_template
import os
import threading
from decimal import *

global hits
global throws
global cycles
global data_lock
data_lock = threading.Lock()
hits = 0
throws = 0
cycles = 0

app = Flask(__name__)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route("/submitwork", methods=['POST'])
def submit():
    global hits
    global throws
    global cycles
    global data_lock

    this_hits = int(request.form['hits'])
    this_throws = int(request.form['throws'])
    with data_lock:
        hits += this_hits
        throws += this_throws
        cycles += 1
    return "Got request:\nHits: {0}\nThrows: {1}\n".format(this_hits, this_throws)

@app.route("/")
def root():
    global hits
    global throws
    global cycles
    global data_lock

    with data_lock:
        local_hits = hits
        local_throws = throws
        local_cycles = cycles

    if (local_throws > 0):
        pi_est = Decimal(local_hits) / Decimal(local_throws) * Decimal(4.0)
    else:
        pi_est = 0
		
    return render_template("index.html.tmpl",throws=local_throws,hits=local_hits,cycles=local_cycles,pi_est=pi_est);

