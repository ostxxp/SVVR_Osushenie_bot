from sqlalchemy import Column, Integer, String

from DB.database import Base, engine


class Prorab(Base):
    __tablename__ = 'prorabs'
    id = Column(Integer, primary_key=True)
    is_filled = Column(Integer)


class Report(Base):
    __tablename__ = 'reports'
    prorab_id = Column(Integer, primary_key=True)
    date = Column(String)
    installers = Column(String)
    object_name = Column(String)
    column = Column(String)
    prorab_name = Column(String)
