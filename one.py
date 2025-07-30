import json
from urllib import request

from fastapi import FastAPI
from pydantic import BaseModel
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
    if key_value is None:
        return Response(content=json.dumps({"message":f"You did not provide the secret key!"}),status_code=403)
    elif key_value != "my-secret-key":
        return Response(content=json.dumps({"message":f"You did not provide the correct secret key : {key_value}"}),status_code=403)
    return Response(content=json.dumps({"message":"Hello Top Secret!"}),status_code=200)

class Secret(BaseModel):
    secret_code : int

@app.get("/secret")
def verify_secret(secret : Secret):
    if len(str(secret.secret_code)) != 4:
        return Response(content=json.dumps({"message":f"The secret code must be 4 digits!"}),status_code=400)
    return Response(content=json.dumps({"message":f"Hello Secret : {secret.secret_code}"}),status_code=200)


@app.get("/welcome")
def welcome_display(request : Request):
    request_type = request.headers.get("accept")
    api_value = request.headers.get("x-api-key")
    if request_type != "text/html" and request_type != "text/plain":
        return Response(content=json.dumps({"message":"Media type not supported! Only plain text and html are supported"}),status_code=400)
    if api_value != "12345678":
        return Response(content=json.dumps({"message":"API key not valid!"}),status_code=403)
    with open("welcome.html","r",encoding="utf-8") as file:
        html_content = file.read()
        return Response(content=html_content,status_code=200,media_type="text/html")


@app.get("{full_path:path}")
def catch_all(full_path : str):
    with open("not_found.html","r",encoding="utf-8") as file:
        html_content = file.read()
        return Response(content=html_content,status_code=404,media_type="text/html")
