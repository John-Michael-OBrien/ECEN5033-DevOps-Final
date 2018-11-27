#!/usr/bin/python

# John-Michael O'Brien
# 11/21/2018
#
# Provides a dashboard page and update API for pi solver jobs


from flask import Flask
from flask import request
from flask import render_template
import os
import redis
from decimal import *

app = Flask(__name__)
# Open a connection to the database
r = redis.Redis(host='pi-solver-redis-service', port=6379, db=0)

# Return static content directly
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

# Get the work results from the solver and update the database
@app.route("/submitwork", methods=['POST'])
def submit():
    # Cache the data from the web request
    this_hits = int(request.form['hits'])
    this_throws = int(request.form['throws'])

    # Create a single transaction and update all of the database values atomically.
    transact = r.pipeline(transaction=True)
    transact.incr("hits",this_hits);
    transact.incr("throws",this_throws);
    transact.incr("cycles",1);
    transact.execute();

    # Send back a basic response
    return "Got request:\nHits: {0}\nThrows: {1}\n".format(this_hits, this_throws)

@app.route("/")
def root():
    # Make an atomic request to the server for the current state
    results = r.mget(["hits","throws","cycles"])
    # Cache the results
    local_hits = results[0]
    local_throws = results[1]
    local_cycles = results[2]
    
    # If we didn't get anything
    if (not local_throws):
        # Replace everything with nulls.
        local_throws=0
        local_hits=0
        local_cycles=0
        pi_est=0
    else:
        # Otherwise, turn our results into bigints.
        local_throws=int(local_throws)
        local_hits=int(local_hits)
        local_cycles=int(local_cycles)

    # If we have actual data
    if (local_throws > 0):
        # Calculate Pi as a Decimal.
        pi_est = Decimal(local_hits) / Decimal(local_throws) * Decimal(4.0)
    else:
        # Otherwise say Pi is 0.
        pi_est = 0
    
    # return our rendered dashboard page. This should be seperated in the long term
    # and AJAX api calls made instead, but this works for now.
    return render_template("index.html.tmpl",throws=local_throws,hits=local_hits,cycles=local_cycles,pi_est=pi_est);

