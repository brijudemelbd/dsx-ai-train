from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, Path, APIRouter
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status

from models import Places
from database import SessionLocal
from routers.auth import get_current_user


router = APIRouter(
    prefix='/admin',
    tags=['admin']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependancy = Annotated[Session, Depends(get_db)]
user_dependancy = Annotated[dict, Depends(get_current_user)]

@router.get("/place", status_code= status.HTTP_200_OK)
async def read_all(user: user_dependancy, db:db_dependancy):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Places).all()


@router.delete("/place/{place_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependancy, db: db_dependancy,place_id:int=Path(gt=0)):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    place_model = db.query(Places).filter(Places.id == place_id).first()
    if place_model is None:
        raise HTTPException(status_code=404, detail="Place not found")
    db.query(Places).filter(Places.id == place_id).delete()
    db.commit()
