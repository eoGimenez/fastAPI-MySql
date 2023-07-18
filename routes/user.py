from fastapi import APIRouter, Depends
from config.db import get_db
from models.user import users
from sqlalchemy.orm import Session
# from schemas.user import User

router = APIRouter(prefix='/api/user', tags=['User'])


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
async def update_user(id: str):
    return 'Buenas desde router'


@router.delete('/{id}')
async def delete_user(id: str):
    return 'Buenas desde router'
