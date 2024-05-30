from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer,primary_key = True, index = True)
    email = Column(String, unique= True)
    username = Column(String, unique= True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default= True)
    role = Column(String)


class Places(Base):
    __tablename__ = 'places'

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String)
    description = Column(String)
    location_url = Column(String)
    image_url = Column(String)
    visited = Column(Boolean, default = False)
    owner_id = Column(Integer, ForeignKey("users.id"))



