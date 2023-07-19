from fastapi import APIRouter, Depends
from config.db import get_db
from models.user import users
from sqlalchemy.orm import Session
from .auth import AuthHandler
from schemas.user import User

router = APIRouter(prefix='/api/user', tags=['User'])

auth_handler = AuthHandler()

@router.get('/')
async def get_users(db: Session = Depends(get_db)):
    all_users = []
    response = db.execute(users.select()).fetchall()
    for doc in response:
        user = (dict(zip(users.columns.keys(), doc)))
        all_users.append(user)
    return all_users


@router.get('/{id}')
async def get_user(id: str, db: Session = Depends(get_db)):
    result = db.execute(
        users.select().where(users.c.id == id)).first()
    return dict(zip(users.columns.keys(), result))

@router.put('/{id}')
async def update_user(id: str, user_details: User, email=Depends(auth_handler.auth_wrapper), db: Session = Depends(get_db)):
    db.execute(
        users.update().values({"name": user_details.name,
                               "email": user_details.email}).where(users.c.id == id))
    found_user = db.execute(
        users.select().where(users.c.id == id)).first()
    created_user = (dict(zip(users.columns.keys(), found_user)))
    db.commit()
    return created_user


@router.delete('/{id}')
async def delete_user(id: str, email=Depends(auth_handler.auth_wrapper), db: Session = Depends(get_db)):
    db.execute(users.delete().where(users.c.id == id))
    db.commit()
    return 'El usuario fue eliminado de la base de datos'
