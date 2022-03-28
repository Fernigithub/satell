from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence , DateTime , PickleType , JSON
from geoalchemy2 import Geometry
from sqlalchemy.orm import sessionmaker
from .config import settings
from sqlalchemy import create_engine
import sqlalchemy as db
metadata = db.MetaData()


Base = declarative_base()
# USER_ID_SEQ = Sequence('user_id_seq')

class area(Base):
    __tablename__ = 'area'
    # id = Column(Integer, USER_ID_SEQ ,server_default=USER_ID_SEQ.next_value())
    name = Column(String(50), primary_key=True)
    date = Column(String(50))
    properties = Column(JSON)
    area = Column(Geometry('POLYGON'))

engine = db.create_engine(settings.db_url)
con = engine.connect()

Session = sessionmaker(bind=engine)
session = Session()

