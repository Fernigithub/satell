from fastapi import FastAPI , HTTPException
import json

# from pyrsistent import optional
from .db import con, area , engine, session
from pydantic import BaseModel
from json import dumps
from sqlalchemy.orm import class_mapper
from sqlalchemy import func
import sqlalchemy as db

import subprocess


app = FastAPI(title="FastAPI, Docker")


def serialize(model):
  """Transforms a model into a dictionary which can be dumped to JSON."""
  columns = [c.key for c in class_mapper(model.__class__).columns]
  return dict((c, str(getattr(model, c))) for c in columns)

class Item(BaseModel):
    name: str
    date: str
    area: str
    properties: dict


@app.get("/retrieve/id/{id}")
async def read_id(id: int):
    try:
        item = session.get(area, id)
        if not item:
            raise HTTPException(status_code=404, detail="area id not found")
    except Exception as e:
        session.rollback()
        return {"Error": e}
    return serialize(item)


@app.post("/save/")
async def create_item(item: Item):
    try:
        valid = session.query(func.ST_IsValid(func.ST_GeomFromText(item.area))).first()[0]
    except:
        session.rollback()
        return {"Error": "The Polygon is not valid"}
    
    try:
        poly = area(name=item.name, date=item.date, area=item.area , properties=item.properties)
        session.add(poly)
        session.commit()
    except:
        session.rollback()
        return {"Error": "The name already exist"}

    return {"Ok": "Saved"}

@app.delete("/delete/{name_str}")
async def delete_item(name_str: str):
    try:
        area_id = session.query(area).filter_by(name=name_str).first()
        if not area_id:
            raise HTTPException(status_code=404, detail="name not found")
        session.delete(area_id)
        session.commit()
    except Exception as e:
        session.rollback()
        return {"Error": e}
    return {"ok": "Deleted"}

@app.get("/retrieve/name/{name}")
async def read_name(name: str):
    try:
        item = session.query(data).filter_by(name=name).all()
        res = []
        for u in item:
            dictio = dict(zip(data.columns.keys(), list(u)))
            res.append(dictio)
            
        sort_res = sorted(res, key=lambda k: k['name'] , reverse=True)
        if not item:
            raise HTTPException(status_code=404, detail="name id not found")
    except Exception as e:
        session.rollback()
        return {"Error": e}
    return str(sort_res)

@app.get("/retrieve/area/{area_str}")
async def read_area(area_str: str):
    try:
        item = session.query(data).all()
        res = []
        for u in item:
            sup = int(session.query(func.ST_Area(u.area)).scalar())
            k = list(data.columns.keys())
            v = list(u)
            k.append("sup")
            v.append(sup)
            inter = session.query(func.ST_Intersects(u.area,func.ST_GeomFromEWKT(area_str)))
            if inter.all()[0][0]:
                dictio = dict(zip(k, v))
                res.append(dictio)
            
        sort_res = sorted(res, key=lambda k: k['sup'] , reverse=True)
    except Exception as e:
        session.rollback()
        return {"Error": e}
    return str(sort_res)

@app.get("/retrieve/inter/{area_str}")
async def inter_area(area_str: str):
    try:
        item = session.query(data).all()
        res = []
        for u in item:
            inter = session.query(func.ST_Intersection(u.area,func.ST_GeomFromEWKT(area_str)))
            new_pol = session.query(func.ST_AsText(inter.all()[0][0]))
            res.append(new_pol.all()[0][0])
    except Exception as e:
        session.rollback()
        return {"Error": e}
    return res

@app.get("/retrieve/prop/{prop_str}")
async def read_prop(prop_str: str):
    try:
        prop_str = prop_str.replace("'",'"')
        prop_str = json.loads(prop_str)
        res = []
        for u in session.query(data).all():
            sup = int(session.query(func.ST_Area(u.area)).scalar())
            k = list(data.columns.keys())
            v = list(u)
            k.append("sup")
            v.append(sup)
            dictio = dict(zip(k, v))
            prop = u.properties
            shared_items = {k: prop[k] for k in prop if k in prop_str and prop[k] == prop_str[k]}
            if shared_items:
                res.append(dictio)
            
        sort_res = sorted(res, key=lambda k: k['sup'] , reverse=True)
    except Exception as e:
        session.rollback()
        return {"Error": e} 
    return str(sort_res)


@app.on_event("startup")
async def startup():
    if con.closed:
        await engine.connect()
    # create a dummy entry
    try:
        area.__table__.drop(engine)
        print("area table dropped")
    except Exception as e:
        pass
    area.__table__.create(engine, checkfirst=True)
    pol1 = area(name='satellogic_1', date = '2022-01-01', area ='POLYGON((0 0,1 0,1 1,0 1,0 0))' , properties = {'name':'satellogic','crop':'wheat'})
    pol2 = area(name='satellogic_2', date = '2022-01-01', area ='POLYGON((0 0,2 0,2 2,0 2,0 0))' , properties = {'name':'satellogic','crop':'soybean'})
    pol3 = area(name='displaced', date = '2022-01-01', area ='POLYGON((2 2,3 2,3 3,2 3,2 2))' , properties = {'name':'satellogic','crop':'soybean'})
    pol4 = area(name='bigger', date = '2022-01-01', area ='POLYGON((1 1,3 1,3 3,1 3,1 1))' , properties = {'name':'satellogic','crop':'maize'})
    session.add_all([pol1,pol2,pol3,pol4])
    session.commit()
    global data
    data = db.Table('area', db.MetaData(engine) ,autoload=True, autoload_with=engine )
    print('Start API')



   

@app.on_event("shutdown")
async def shutdown():
    if not con.closed:
        await con.close()