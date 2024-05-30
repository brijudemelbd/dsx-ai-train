from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

USER = "root"
PASS = "admin12345"
HOST = "localhost"
PORT = 3306
MYSQL_DATABASE_URL = 'mysql+pymysql://{0}:{1}@{2}:{3}/dell'.format(USER, PASS, HOST, PORT)


engine = create_engine(MYSQL_DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()
