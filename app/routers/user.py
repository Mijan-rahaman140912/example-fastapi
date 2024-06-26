from fastapi import FastAPI,Response,status,HTTPException, Depends, APIRouter
from app.oauth2 import get_current_user
from . . import models,schemas,utils, oauth2
from . . database import get_db
from sqlalchemy.orm import Session



router = APIRouter(
    prefix="/users",
    tags=['Users']
)





@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate,db: Session = Depends(get_db),):  
    hashed_password=utils.hash(user.password)
    user.password=hashed_password
  
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model=schemas.UserResponse)
def get_user( id: int,db: Session = Depends(get_db),current_user: int = Depends
                 (oauth2.get_current_user)):
   
    users=db.query(models.User).filter(models.User.id == id).first()
       
    if not users:
       
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with {id} was not found")
    
    return users




