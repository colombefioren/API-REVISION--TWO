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


