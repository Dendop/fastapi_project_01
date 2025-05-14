from fastapi import FastAPI,APIRouter, Response, HTTPException, status, Depends
from .. import database, model, schema, oauth2
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: schema.Vote, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    vote_query = db.query(model.Votes).filter(model.Votes.post_id == vote.post_id, model.Votes.user_id == current_user.id)
    found_vote = vote_query.first()
    post = db.query(model.Post).filter(model.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post has not been found.")
    
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"{current_user.id} has already voted on {vote.post_id}")
  
        new_vote = model.Votes(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Voting succesfull"}
        
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist")
        
        db.delete(found_vote)
        db.commit()
        return {"message": "Vote deleted succesfull"}