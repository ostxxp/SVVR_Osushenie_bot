from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Table, PrimaryKeyConstraint
from sqlalchemy.orm import relationship, Session

from DB.database import Base, engine


class Prorab(Base):
    __tablename__ = 'prorabs'
    id = Column(Integer, primary_key=True)
    is_filled = Column(Integer)


class Report(Base):
    __tablename__ = 'reports'
    prorab_id = Column(Integer, primary_key=True)
    date = Column(String, primary_key=True)
    __table_args__ = (
        PrimaryKeyConstraint('prorab_id', 'date'),
        {}
    )
