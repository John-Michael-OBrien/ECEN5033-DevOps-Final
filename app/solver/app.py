import requests
import random

print("Starting tosses...")

tests = 10000

while (True):
    throws = 0
    hits = 0

    for i in range(0,tests):
        # Throw a dart
        x=random.SystemRandom().random()
        y=random.SystemRandom().random()
        throws += 1

        # If it lands inside our unit circle sector
        if (x*x+y*y<=1):
            # Mark the hit
            hits += 1

    payload = {"hits":hits, "throws":throws}

    print("Threw {0} darts. Hit {1} times.".format(throws,hits))
    print("Sending request...")
    r = requests.post("http://pi-solver-controller-service/submitwork",data=payload)
    print("Got response")
    print(r.text)
