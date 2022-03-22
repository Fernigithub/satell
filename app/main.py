from fastapi import FastAPI , HTTPException
import json
from app.db import con, area , engine, session, db
from pydantic import BaseModel
from typing import Optional
from json import dumps
from sqlalchemy.orm import class_mapper


app = FastAPI(title="FastAPI, Docker")



def serialize(model):
  """Transforms a model into a dictionary which can be dumped to JSON."""
  # first we get the names of all the columns on your model
  columns = [c.key for c in class_mapper(model.__class__).columns]
  # then we return their values in a dict
  return dict((c, getattr(model, c)) for c in columns)

class Item(BaseModel):
    name: str
    date: str
    area: str
    properties: dict

@app.get("/")
async def read_root():
    data = db.Table('area', db.MetaData(engine) ,autoload=True,autoload_with=engine)
    return data.columns.keys()

@app.get("/retrieve/{id}")
async def read_id():
    item = session.get(area, id)
    return serialize(item)

@app.post("/save/")
async def create_item(item: Item):
    try:
        poly = area(name=item.name, date=item.date, area=item.area , properties=item.properties)
        session.add(poly)
        session.commit()
    except Exception as e:
        print(e)
        return {"error": e}
    return "saved"

@app.delete("/delete/{area_id}")
def delete_item(area_id: int):
    area_id = session.get(area, area_id)
    if not area_id:
        raise HTTPException(status_code=404, detail="area id not found")
    session.delete(area_id)
    session.commit()
    return {"ok": True}

@app.on_event("startup")
async def startup():
    if con.closed:
        await engine.connect()
    # create a dummy entry
    try:
        area.__table__.drop(engine)
        print("se elimino la tabla")
    except Exception as e:
        print('no se elimino la tabla',e)
    area.__table__.create(engine)
    # poly = area(name='satellogic', date = '2022-01-01', area ='POLYGON((0 0,1 0,1 1,0 1,0 0))' , properties = {'name':'satellogic'})
    # session.add(poly)
    # session.commit()
    

@app.on_event("shutdown")
async def shutdown():
    if not con.closed:
        await con.close()