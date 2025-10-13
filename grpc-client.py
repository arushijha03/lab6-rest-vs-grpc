#!/usr/bin/env python3
from __future__ import print_function
import sys, time, random, base64

import grpc
import lab6_pb2, lab6_pb2_grpc

def do_add(stub, debug=False):
    req = lab6_pb2.addMsg(a=5, b=10)
    resp = stub.Add(req)
    if debug: print(resp)

def do_raw_image(stub, debug=False):
    with open('Flatirons_Winter_Sunrise_edit_2.jpg','rb') as f:
        img = f.read()
    req = lab6_pb2.rawImageMsg(img=img)
    resp = stub.RawImage(req)
    if debug: print(resp)

def do_json_image(stub, debug=False):
    with open('Flatirons_Winter_Sunrise_edit_2.jpg','rb') as f:
        img_b64 = base64.b64encode(f.read()).decode('ascii')
    req = lab6_pb2.jsonImageMsg(img=img_b64)
    resp = stub.JsonImage(req)
    if debug: print(resp)

def do_dot_product(stub, debug=False):
    a = [random.random() for _ in range(100)]
    b = [random.random() for _ in range(100)]
    req = lab6_pb2.dotProductMsg(a=a, b=b)
    resp = stub.DotProduct(req)
    if debug: print(resp)

def main():
    if len(sys.argv) < 4:
        print(f"Usage: {sys.argv[0]} <server ip> <cmd> <reps>")
        print("where <cmd> is one of add, rawImage, jsonImage, dotProduct")
        sys.exit(1)

    host, cmd, reps = sys.argv[1], sys.argv[2], int(sys.argv[3])
    target = f"{host}:50051"
    print(f"Running {reps} reps against {target}")

    with grpc.insecure_channel(target) as channel:
        stub = lab6_pb2_grpc.Lab6Stub(channel)

        if cmd == 'add':
            t0 = time.perf_counter()
            for _ in range(reps): do_add(stub)
            print("Took", ((time.perf_counter()-t0)/reps)*1000, "ms per operation")
        elif cmd == 'rawImage':
            t0 = time.perf_counter()
            for _ in range(reps): do_raw_image(stub)
            print("Took", ((time.perf_counter()-t0)/reps)*1000, "ms per operation")
        elif cmd == 'jsonImage':
            t0 = time.perf_counter()
            for _ in range(reps): do_json_image(stub)
            print("Took", ((time.perf_counter()-t0)/reps)*1000, "ms per operation")
        elif cmd == 'dotProduct':
            t0 = time.perf_counter()
            for _ in range(reps): do_dot_product(stub)
            print("Took", ((time.perf_counter()-t0)/reps)*1000, "ms per operation")
        else:
            print("Unknown option", cmd)

if __name__ == "__main__":
    main()
