#!/usr/bin/env python3
from __future__ import print_function
import requests
import json
import time
import sys
import base64
import jsonpickle  # kept to match starter imports (not strictly required here)
import random

def doRawImage(addr, debug=False):
    # Prepare headers for HTTP request (file is a JPG in the lab assets)
    headers = {'content-type': 'image/jpeg'}
    img = open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb').read()
    # Send HTTP request with image and receive response
    image_url = addr + '/api/rawimage'
    response = requests.post(image_url, data=img, headers=headers)
    if debug:
        print("Response is", response)
        print(json.loads(response.text))

def doAdd(addr, debug=False):
    headers = {'content-type': 'application/json'}
    # Send request; body is ignored by server for add
    add_url = addr + "/api/add/5/10"
    response = requests.post(add_url, headers=headers)
    if debug:
        print("Response is", response)
        print(json.loads(response.text))

def doDotProduct(addr, debug=False):
    headers = {'content-type': 'application/json'}
    # Generate two length-100 vectors with values in [0,1)
    a = [random.random() for _ in range(100)]
    b = [random.random() for _ in range(100)]
    url = addr + "/api/dotproduct"
    payload = {"a": a, "b": b}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if debug:
        print("Response is", response)
        print(json.loads(response.text))

def doJsonImage(addr, debug=False):
    headers = {'content-type': 'application/json'}
    # Read image bytes and base64-encode into JSON
    with open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb') as f:
        img_bytes = f.read()
    img_b64 = base64.b64encode(img_bytes).decode('ascii')
    url = addr + "/api/jsonimage"
    payload = {"image": img_b64}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if debug:
        print("Response is", response)
        print(json.loads(response.text))

if len(sys.argv) < 3:
    print(f"Usage: {sys.argv[0]} <server ip> <cmd> <reps>")
    print(f"where <cmd> is one of add, rawImage, dotProduct or jsonImage")
    print(f"and <reps> is the integer number of repetitions for measurement")
    sys.exit(1)

host = sys.argv[1]
cmd = sys.argv[2]
reps = int(sys.argv[3])

addr = f"http://{host}:5000"
print(f"Running {reps} reps against {addr}")

if cmd == 'rawImage':
    start = time.perf_counter()
    for _ in range(reps):
        doRawImage(addr)
    delta = ((time.perf_counter() - start)/reps)*1000
    print("Took", delta, "ms per operation")
elif cmd == 'add':
    start = time.perf_counter()
    for _ in range(reps):
        doAdd(addr)
    delta = ((time.perf_counter() - start)/reps)*1000
    print("Took", delta, "ms per operation")
elif cmd == 'jsonImage':
    start = time.perf_counter()
    for _ in range(reps):
        doJsonImage(addr)
    delta = ((time.perf_counter() - start)/reps)*1000
    print("Took", delta, "ms per operation")
elif cmd == 'dotProduct':
    start = time.perf_counter()
    for _ in range(reps):
        doDotProduct(addr)
    delta = ((time.perf_counter() - start)/reps)*1000
    print("Took", delta, "ms per operation")
else:
    print("Unknown option", cmd)
