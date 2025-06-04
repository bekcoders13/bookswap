# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# import pymysql
#
# engine = create_engine('mysql+pymysql://host5504_boss:asilbek2004@localhost/asilbek11_tg_bot', pool_pre_ping=True)
# SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
# Base = declarative_base()
#
#
# def database():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

engine = sqlalchemy.create_engine("sqlite:///./tr_bot.db",
                                  connect_args={"check_same_thread": False})

SessionLocal = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
