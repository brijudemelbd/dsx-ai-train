from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

USER = "root"
PASSWORD = "admin12345"
HOST = "localhost"
PORT = 3306
MYSQL_DATABASE_URL = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/dell"

engine = create_engine(MYSQL_DATABASE_URL)

SessionLocal = sessionmaker(autoflush = False, autocommit= False, bind=engine)

Base = declarative_base()
