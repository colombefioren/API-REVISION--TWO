import json
from typing import List, Optional

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

@app.get("/events")
def get_events():
    return Response(content=json.dumps(serialized_events_store()),status_code=200,media_type="application/json")

@app.post("/events")
def add_event(event_list : List[Event]):
    for event in event_list:
        events_store.append(event)
    return Response(content=json.dumps(serialized_events_store()),status_code=201,media_type="application/json")

@app.get("/events/{events_id}")
def get_event(events_id : int):
    for event in events_store:
        if event.id == events_id:
            return Response(content=json.dumps(event.model_dump()),status_code=200,media_type="application/json")
    return Response(content=json.dumps({"message":f"Event with id {events_id} not found!"}),status_code=404,media_type="application/json")

class EventUpdated(BaseModel):
    id : Optional[int] = None,
    name : Optional[str] = None,
    start_date : Optional[str] = None,
    end_date : Optional[str] = None


@app.patch("/events/{events_id}")
def update_event(events_id : int,event_updated : EventUpdated):
    for event in events_store:
        if event.id == events_id:
            if event_updated.id is not None:
                event.id = event_updated.id
            if event_updated.name is not None:
                event.name = event_updated.name
            if event_updated.start_date is not None:
                event.start_date = event_updated.start_date
            return Response(content=json.dumps(serialized_events_store()),status_code=200,media_type="application/json")
    return Response(content=json.dumps({"message":f"Event with id {events_id} not found!"}),status_code=404,media_type="application/json")