#!/usr/bin/env python3
import base64, io
from concurrent import futures

import grpc
import lab6_pb2, lab6_pb2_grpc
from PIL import Image

class Lab6Service(lab6_pb2_grpc.Lab6Servicer):
    def Add(self, request, context):
        s = int(request.a) + int(request.b)
        return lab6_pb2.addReply(sum=s)

    def RawImage(self, request, context):
        try:
            img = Image.open(io.BytesIO(request.img))
            return lab6_pb2.imageReply(width=img.size[0], height=img.size[1])
        except Exception:
            return lab6_pb2.imageReply(width=0, height=0)

    def DotProduct(self, request, context):
        a = request.a
        b = request.b
        if len(a) != len(b):
            context.set_details("vectors must be the same length")
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return lab6_pb2.dotProductReply(dotproduct=0.0)
        dp = sum(float(x) * float(y) for x, y in zip(a, b))
        return lab6_pb2.dotProductReply(dotproduct=dp)

    def JsonImage(self, request, context):
        try:
            img_bytes = base64.b64decode(request.img)
            img = Image.open(io.BytesIO(img_bytes))
            return lab6_pb2.imageReply(width=img.size[0], height=img.size[1])
        except Exception:
            return lab6_pb2.imageReply(width=0, height=0)

def serve(bind_addr="0.0.0.0:50051"):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=8))
    lab6_pb2_grpc.add_Lab6Servicer_to_server(Lab6Service(), server)
    server.add_insecure_port(bind_addr)
    server.start()
    print(f"gRPC server listening on {bind_addr}")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
