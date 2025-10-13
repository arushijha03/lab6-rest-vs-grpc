#!/usr/bin/env python3

##
## Sample Flask REST server implementing two methods
##
## Endpoint /api/image is a POST method taking a body containing an image
## It returns a JSON document providing the 'width' and 'height' of the
## image that was provided. The Python Image Library (pillow) is used to
## proce#ss the image
##
## Endpoint /api/add/X/Y is a post or get method returns a JSON body
## containing the sum of 'X' and 'Y'. The body of the request is ignored
##
##
from flask import Flask, request, Response
import jsonpickle
from PIL import Image
import base64
import io
import logging

# Initialize the Flask application
app = Flask(__name__)

# Quieter werkzeug logs (optional)
log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)

@app.route('/api/add/<int:a>/<int:b>', methods=['GET', 'POST'])
def add(a, b):
    # NOTE: starter expected sum as a string; we keep that for compatibility
    response = {'sum': str(a + b)}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

# route http posts to this method (binary image in the body)
@app.route('/api/rawimage', methods=['POST'])
def rawimage():
    try:
        io_buf = io.BytesIO(request.data)
        img = Image.open(io_buf)
        response = {'width': img.size[0], 'height': img.size[1]}
    except Exception as e:
        response = {'width': 0, 'height': 0, 'error': str(e)}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/api/dotproduct', methods=['POST'])
def dotproduct():
    try:
        data = request.get_json(force=True, silent=False)
        a = data.get('a', [])
        b = data.get('b', [])
        if not isinstance(a, list) or not isinstance(b, list):
            raise ValueError("a and b must be lists")
        if len(a) != len(b):
            raise ValueError("vectors must be the same length")
        dp = sum(float(x) * float(y) for x, y in zip(a, b))
        response = {'dotproduct': dp}
    except Exception as e:
        response = {'error': str(e)}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

# JSON payload with base64-encoded image bytes
@app.route('/api/jsonimage', methods=['POST'])
def jsonimage():
    try:
        data = request.get_json(force=True, silent=False)
        img_b64 = data.get('image', None)
        if not img_b64:
            raise ValueError("missing 'image' in JSON payload")
        img_bytes = base64.b64decode(img_b64)
        img = Image.open(io.BytesIO(img_bytes))
        response = {'width': img.size[0], 'height': img.size[1]}
    except Exception as e:
        response = {'width': 0, 'height': 0, 'error': str(e)}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

if __name__ == "__main__":
    # Bind on 0.0.0.0 so other VMs can reach it
    app.run(host="0.0.0.0", port=5000)