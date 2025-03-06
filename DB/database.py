from sqlalchemy import create_engine, Column, Integer, String, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///../DB/db.db')
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()
