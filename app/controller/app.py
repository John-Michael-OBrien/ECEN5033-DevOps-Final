#!/usr/bin/python

# John-Michael O'Brien
# 09/24/2018
#
# A basic web service.

from flask import Flask
from flask import request
from flask import render_template
import os
import redis
from decimal import *

app = Flask(__name__)
r = redis.Redis(host='pi-solver-redis-service', port=6379, db=0)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route("/submitwork", methods=['POST'])
def submit():
    this_hits = int(request.form['hits'])
    this_throws = int(request.form['throws'])

    transact = r.pipeline(transaction=True)
    transact.incr("hits",this_hits);
    transact.incr("throws",this_throws);
    transact.incr("cycles",1);
    transact.execute();

    return "Got request:\nHits: {0}\nThrows: {1}\n".format(this_hits, this_throws)

@app.route("/")
def root():
    results = r.mget(["hits","throws","cycles"])
    local_hits = results[0]
    local_throws = results[1]
    local_cycles = results[2]
	
    if (not local_throws):
        local_throws=0
        local_hits=0
        local_cycles=0
        pi_est=0
    else:
        local_throws=int(local_throws)
        local_hits=int(local_hits)
        local_cycles=int(local_cycles)

	
    if (local_throws > 0):
        pi_est = Decimal(local_hits) / Decimal(local_throws) * Decimal(4.0)
    else:
        pi_est = 0

    return render_template("index.html.tmpl",throws=local_throws,hits=local_hits,cycles=local_cycles,pi_est=pi_est);

