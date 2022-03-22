from fastapi import FastAPI
import json
from pydantic import BaseModel
from typing import Optional


app = FastAPI(title="FastAPI, Docker")

class Item(BaseModel):
    name: str
    date: str
    area: str
    properties: dict


@app.post("/save/")
async def create_item(item: Item):
    return item


