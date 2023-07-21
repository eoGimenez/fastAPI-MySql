import random
from fastapi import APIRouter, Depends, HTTPException, status, Response
from starlette.status import HTTP_204_NO_CONTENT
import string
from models.user import users
from sqlalchemy.orm import Session
from config.db import get_db
from .auth import AuthHandler
from models.post import posts
from schemas.post import Post


router = APIRouter(prefix='/api/post', tags=['Post'])


def id_generator():
    chars = string.ascii_letters
    digits = string.digits
    id = "".join(random.choices(f'{chars}{digits}', k=28))
    return id


auth_handler = AuthHandler()


@router.get('/')
async def get_posts(page,  post_num: int, db: Session = Depends(get_db)):
    all_posts = []
    # response = db.execute(posts.select()).fetchall()
    response = db.execute(posts.select()).fetchmany(size=post_num)
    print(response)
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


@router.get('/{id}', response_model=Post)
async def get_post(id: str, db: Session = Depends(get_db), id_token=Depends(auth_handler.auth_wrapper)):
    found_post: Post = db.execute(
        posts.select().where(posts.c.id == id)).first()
    if (not found_post):
        raise HTTPException(
            404, 'Surgio un problema y no pudimos encontrar ese post, intentelo nuevamente')
    post = dict(zip(posts.columns.keys(), found_post))
    return post


@router.put('/{id}', response_model=Post)
async def update_post(id: str, post_details: Post, db: Session = Depends(get_db), id_token=Depends(auth_handler.auth_wrapper)):
    found_post: Post = dict(zip(posts.columns.keys(), db.execute(
        posts.select().where(posts.c.id == id)).first()))
    if (found_post["author"] == id_token):
        db.execute(posts.update().values(
            {"place": post_details.place, "comment": post_details.comment, "image": post_details.image}).where(posts.c.id == id))
        db.commit()
        updated_post: Post = dict(zip(posts.columns.keys(), db.execute(
            posts.select().where(posts.c.id == id)).first()))
        return updated_post
    return "No tienes permisos para realizar esa acción."


@router.delete('/{id}')
async def delete_post(id: str, db: Session = Depends(get_db), id_token=Depends(auth_handler.auth_wrapper)):
    found_post: Post = db.execute(
        posts.select().where(posts.c.id == id)). first()
    if (not found_post):
        raise HTTPException(
            404, "Fue imposible encontrar el post a eliminar, por favor espere un momento y vuelva a intentarlo")
    if (found_post.author != id_token):  # agregar checkeo de admin.
        raise HTTPException(
            401, 'No puede eliminar o modificar posts de otros usuarios sin permisos de ADMIN')
    db.execute(posts.delete().where(posts.c.id == id))
    db.commit()
    return
