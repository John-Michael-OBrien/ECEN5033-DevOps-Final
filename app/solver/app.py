#!/usr/bin/python

# John-Michael O'Brien
# 11/21/2018
#
# Throws darts at quadrant 1 of a dart board and reports the results
# to an upstream API server via service discovery.

import requests
import random

print("Starting tosses...")

# Set the number of throws to make per report
tests = 10000

# Start throwing
while (True):
    throws = 0
    hits = 0

    # for each test we plan to do
    for i in range(0,tests):
        # Throw a dart
        x=random.SystemRandom().random()
        y=random.SystemRandom().random()
        throws += 1

        # If it lands inside our unit circle sector
        if (x*x+y*y<=1):
            # Mark the hit
            hits += 1

    # Build up the report
    payload = {"hits":hits, "throws":throws}

    # Make the report to the server.
    print("Threw {0} darts. Hit {1} times.".format(throws,hits))
    print("Sending request...")
    r = requests.post("http://pi-solver-controller-service/submitwork",data=payload)
    print("Got response")
    print(r.text)
