import json

from fastapi import FastAPI
from starlette.responses import Response

app = FastAPI();

@app.get("/")
def read_root():
    return Response(content=json.dumps({"message" : "Hello World!"}),status_code=200,media_type="application/json")

