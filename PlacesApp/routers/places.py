from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, Path, APIRouter
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status

from models import Places
from database import SessionLocal
from routers.auth import get_current_user


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependancy = Annotated[Session, Depends(get_db)]
user_dependancy = Annotated[dict, Depends(get_current_user)]

class PlacesRequest(BaseModel):
    name: str = Field(min_length = 3)
    description: str = Field(min_length=3, max_length=100)
    location_url: str = Field(min_length=3, max_length=500)
    image_url: str = Field(min_length=3, max_length=100)
    visited: bool

@router.get("/", status_code= status.HTTP_200_OK)
async def home(db: db_dependancy):
    return "Welcome to Places DB"

@router.get("/places", status_code= status.HTTP_200_OK)
async def read_all(user: user_dependancy,db: db_dependancy):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Places).filter(Places.owner_id == user.get('id')).all()

@router.get("/place/{place_id}", status_code= status.HTTP_200_OK)
async def read_place_by_id(user:user_dependancy ,db: db_dependancy, place_id: int = Path(gt = 0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    place_model = db.query(Places).filter(Places.id == place_id).filter(Places.owner_id == user.get('id')).first()
    if place_model is not None:
        return place_model
    raise HTTPException(status_code=404, detail="Place not found")

@router.post("/place", status_code=status.HTTP_201_CREATED)
async def create_place(user: user_dependancy ,db: db_dependancy, place_request: PlacesRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    place_model = Places(**place_request.dict(), owner_id= user.get("id"))
    db.add(place_model)
    db.commit()

@router.put("/place/{place_id}", status_code= status.HTTP_204_NO_CONTENT)
async def update_place(user: user_dependancy ,db: db_dependancy, place_request: PlacesRequest, place_id: int= Path(gt = 0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    place_model = db.query(Places).filter(Places.id == place_id).filter(Places.owner_id == user.get('id')).first()
    if place_model is None:
        raise HTTPException(status_code= 404, detail= "Place not found")
    place_model.name = place_request.name
    place_model.description = place_request.description
    place_model.image_url = place_request.image_url
    place_model.location_url = place_request.location_url
    place_model.visited = place_request.visited

    db.add(place_model)
    db.commit()

@router.delete("/place/{place_id}", status_code= status.HTTP_204_NO_CONTENT)
async def delete_place(user: user_dependancy,db: db_dependancy, place_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    place_model = db.query(Places).filter(Places.id == place_id).filter(Places.owner_id == user.get('id')).first()
    if place_model is None:
        raise HTTPException(status_code=404, detail="Place not found")
    db.query(Places).filter(Places.id == place_id).delete()
    db.commit()

