import json

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/version")
def get_version(request : Request):
    accept_type = request.headers.get("accept")
    if accept_type != "application/json":
        return Response(content=json.dumps({"message": "Unrequired media type!"}),status_code=406,media_type="application/json")
    return Response(content=json.dumps({"version":"1.0.0"}),status_code=200,media_type="application/json")
