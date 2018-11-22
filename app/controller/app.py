#!/usr/bin/python

# John-Michael O'Brien
# 09/24/2018
#
# A basic web service.

from flask import Flask
from flask import request
import os
import threading

global hits
global throws
global cycles
global data_lock
data_lock = threading.Lock()
hits = 0
throws = 0
cycles = 0

app = Flask(__name__)

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
    return "Got request:\nHits: {0}\nThrows: {1}\n".format(this_hits, this_thows)

@app.route("/")
def root():
    global hits
    global throws
    global cycles
    global data_lock

    with data_lock:
        local_hits = hits
        local_thows = throws
        local_cycles = cycles

    return "Current Statistics:\nHits: {0}\nThrows: {1}\nCycles: {2}\n".format(local_hits, local_thows, local_cycles)
