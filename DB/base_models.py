from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Table
from sqlalchemy.orm import relationship, Session

from DB.database import Base, engine

class Prorab(Base):
    __tablename__ = 'prorabs'
    id = Column(Integer, primary_key=True)
    is_filled = Column(Integer)

class Installer(Base):
    __tablename__ = 'installers'
    id = Column(Integer, primary_key=True)
