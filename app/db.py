# import databases
# import ormar
# import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence , DateTime , PickleType , JSON
from geoalchemy2 import Geometry
from sqlalchemy.orm import sessionmaker
from .config import settings
from sqlalchemy import create_engine
import sqlalchemy as db
# database = databases.Database(settings.db_url)
metadata = db.MetaData()


# engine = create_engine('postgresql://fastapi_satellogic:fastapi_satellogic@localhost:5433/fastapi_satellogic')

Base = declarative_base()
USER_ID_SEQ = Sequence('user_id_seq')
class area(Base):
    __tablename__ = 'area'
    id = Column(Integer, USER_ID_SEQ ,primary_key=True ,server_default=USER_ID_SEQ.next_value())
    name = Column(String(50))
    date = Column(DateTime(timezone=True))
    properties = Column(JSON)
    # properties = Column(PickleType)
    area = Column(Geometry('POLYGON'))

engine = db.create_engine(settings.db_url)
metadata.create_all(engine)
con = engine.connect()


Session = sessionmaker(bind=engine)
session = Session()

