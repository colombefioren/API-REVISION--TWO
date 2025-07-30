import json

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

app = FastAPI()

@app.get("/")
def read_root(request : Request,name: str = "Non défini(e)",is_teacher : bool = False):
    accept_type = request.headers.get("accept")
    if accept_type != "text/plain" and accept_type != "text/html":
        return Response(content=json.dumps({"message":"Media type not supported!"}),status_code=400)
    if is_teacher:
         return Response(content=json.dumps({"message":f"Hello teacher {name}!"}),status_code=200)
    if name != "Non défini(e)":
        return Response(content=json.dumps({"message":f"Hello {name}!"}),status_code=200)
    return Response(content=json.dumps({"message":f"Hello World!"}),status_code=200)

@app.get("/top-secret")
def read_top_secret(request : Request):
    key_value = request.headers.get("Authorization")
    if key_value is None or key_value != "my-secret-key":
        return Response(content=json.dumps({"message":f"{key_value} is not the secret key!"}),status_code=403)
    return Response(content=json.dumps({"message":"Hello Top Secret!"}),status_code=200)


