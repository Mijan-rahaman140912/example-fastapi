from typing import List,Optional
from fastapi import FastAPI,Response,status,HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from . . import models,schemas, oauth2
from . . database import get_db
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/",response_model=List[schemas.PostVote])
def get(db: Session = Depends(get_db),current_user: int = Depends
                 (oauth2.get_current_user),limit: int=10,skip: int= 0, search:Optional[str]= ""):
    
    #posts=db.query(models.post).filter(models.post.title.contains(search)).limit(limit).offset(skip).all()#filter(models.post.owner_id == current_user.id).all()
    
    posts = db.query(models.post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Vote.post_id == models.post.id,isouter=True).group_by(models.post.id).filter(
            models.post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate,db: Session = Depends(get_db),current_user: int = Depends
                 (oauth2.get_current_user)):  
    
   
  
    post = models.post(owner_id = current_user.id, **post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.get("/{id}",response_model=schemas.PostVote)
def get_posts( id: int,db: Session = Depends(get_db),current_user: int = Depends
                 (oauth2.get_current_user)):
   
    #posts=db.query(models.post).filter(models.post.id == id).first()
    posts= db.query(models.post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Vote.post_id == models.post.id,isouter=True).group_by(models.post.id).first()
       
    if not posts:
       
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} was not found")
        
    # if posts.owner_id != current_user.id:
       # raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                           # detail=f"not authorize to perform action")
        
    
    return posts

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)

def delete_posts(id: int,db: Session = Depends(get_db),current_user: int = Depends
                 (oauth2.get_current_user)):
   
    #cursor.execute("""DELETE FROM posts WHERE  id= %s RETURNING *""",(str(id),))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    
    
    deleted_post_query = db.query(models.post).filter(models.post.id == id)
    deleted_post = deleted_post_query.first()
       
    
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} does not exit ")
        
    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"not authorize to perform action")
        
    deleted_post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

@router.put("/{id}",response_model=schemas.PostResponse)
def update_posts(id: int, updated_post:schemas.PostCreate,db: Session = Depends(get_db),current_user: int = Depends
                 (oauth2.get_current_user)):
    #cursor.execute("""UPDATE posts SET title= %s, content=%s WHERE id=%s returning *""",
                   #(post.title,post.content,(str(id))))
    #updated_post= cursor.fetchone()
    #conn.commit()
    query_post=db.query(models.post).filter(models.post.id == id)
    post=query_post.first()
    
    if post == None:
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} does not exit ")
    
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"not authorize to perform action")
    
    query_post.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    
    return query_post.first()
