from fastapi import APIRouter, Depends, HTTPException
from config.db import get_db
from models.post import posts
from sqlalchemy.orm import Session
from .auth import AuthHandler
from schemas.post import Post

router = APIRouter(prefix='/api/post', tags=['Post'])

auth_handler = AuthHandler()


@router.get('/', response_model=Post)
async def get_posts(db: Session = Depends(get_db)):
    all_posts = []
    response = db.execute(posts.select().fetchall())
    for doc in response:
        post = dict(zip(posts.columns.keys(), doc))
        all_posts.append(post)
    return all_posts


@router.post('/', response_model=Post)
async def create_post(post_details: Post, db: Session = Depends(get_db), id_token=Depends(auth_handler.auth_wrapper)):

    new_post = {"place": post_details.place, "comment": post_details.comment,
                "image": post_details.image, "autho": id_token}
