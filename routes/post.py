from fastapi import APIRouter, Depends, HTTPException
import random
import string
from config.db import get_db
from models.post import posts
from models.user import users
from sqlalchemy.orm import Session
from .auth import AuthHandler
from schemas.post import Post


router = APIRouter(prefix='/api/post', tags=['Post'])


def id_generator():
    chars = string.ascii_letters
    digits = string.digits
    id = "".join(random.choices(f'{chars}{digits}', k=28))
    return id


auth_handler = AuthHandler()


@router.get('/')
async def get_posts(db: Session = Depends(get_db)):
    all_posts = []
    response = db.execute(posts.select()).fetchall()
    for doc in response:
        post = dict(zip(posts.columns.keys(), doc))
        all_posts.append(post)
    return all_posts


@router.post('/', response_model=Post)
async def create_post(post_details: Post, db: Session = Depends(get_db), id_token=Depends(auth_handler.auth_wrapper)):
    new_id = id_generator()
    new_post = {"id": new_id, "place": post_details.place, "comment": post_details.comment,
                "image": post_details.image, "author": id_token}
    db.execute(posts.insert().values(new_post))
    db.commit()
    found_post: Post = db.execute(
        posts.select().where(posts.c.id == new_id)).first()
    created_post = (dict(zip(posts.columns.keys(), found_post)))
    return created_post

@router.put('/{id}', response_model=Post)
async def update_post(id: str, post_details : Post, db: Session = Depends(get_db), id_token=Depends(auth_handler.auth_wrapper)):
    return "edit"

@router.delete('/{id}')
async def delete_post(id: str, db: Session = Depends(get_db), id_token=Depends(auth_handler.auth_wrapper)):
    return "delete"