from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Observation(Base):
    __tablename__ = "observations"
    id = Column(Integer, primary_key=True)
    mass = Column(String)

