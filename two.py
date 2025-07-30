import json
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
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

class Event(BaseModel):
    id : int
    name : str
    start_date : str
    end_date : str

events_store : List[Event] = []

def serialized_events_store():
    converted_event = []
    for event in events_store:
        converted_event.append(event.model_dump())
    return converted_event

@app.post("/events")
def add_event(event_list : List[Event])
    for event in event_list:
        events_store.append(event)
    return Response(content=json.dumps(serialized_events_store()),status_code=201,media_type="application/json")

@app.get("/events/{events_id}")
def get_event(events_id : int):
    for event in events_store:
        if event.id == events_id:
            return Response(content=json.dumps(event.model_dump()),status_code=200,media_type="application/json")
    return Response(content=json.dumps({"message":f"Event with id {events_id} not found!"}),status_code=404,media_type="application/json")
