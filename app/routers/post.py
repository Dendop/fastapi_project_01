from .. import schema, model, oauth2
from ..database import get_db
from fastapi import FastAPI, Depends, Response, status, HTTPException, APIRouter
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get('/', response_model=List[schema.PostWithVotes])
def get_posts(db: Session = Depends(get_db), limit: int = 10): #limit gives a user option to specify how many posts they want to see
    # cursor.execute("""SELECT * FROM "posts" WHERE "id" = 3 """)
    # posts = cursor.fetchall()
    posts = db.query(model.Post).limit(limit).all()
    
    result = db.query(model.Post, func.count(model.Votes.post_id).label("votes")).join(model.Votes, model.Votes.post_id == model.Post.id).group_by(model.Post.id).all()
    response = [{"post": row[0], "votes": row[1]} for row in result]
    return response

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.ResponsePost)
def create_posts(post: schema.PostBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO "posts" ("title","content","published")
    #                   VALUES (%s, %s, %s)
    #                   RETURNING * """,
    #                   (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    #new_post = model.Post(title=post.title, content=post.content, published=post.published) BETTER solution to change into Python dict and unpack
    
    new_post = model.Post(user_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # return the data to postman or browser(client)
    return new_post

@router.get('/{id}', response_model=schema.ResponsePost)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM "posts" WHERE "id" = %s """, (id,))
    # post = cursor.fetchone()
    post = db.query(model.Post).filter(model.Post.id == id).first()
  
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} was not found")
    return post

@router.delete('/{id}')
def delete_post(id: int, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    
    post = db.query(model.Post).efiltr(model.Post.id == id).first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} was not found")
        
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to delete the post")
    
    db.delete(post)
    db.refresh(post)
    db.commit()
    
    
    
    return post 

@router.put('/{id}', response_model=schema.ResponsePost)
def update_post(id: int, updated_post: schema.PostBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE "posts" SET "title"= %s, "content"= %s, published= %s WHERE "id" = %s RETURNING *""", 
    #                (post.title, post.content, post.published, (id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    existing_post = db.query(model.Post).filter(model.Post.id == id)
    post = existing_post.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} was not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to update the post")
    
    existing_post.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return existing_post.first()