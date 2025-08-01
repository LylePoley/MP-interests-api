# db.py
from sqlmodel import SQLModel, create_engine, Session

engine = create_engine("sqlite:///members.db")  # or Postgres URI

def get_session():
    return Session(engine)