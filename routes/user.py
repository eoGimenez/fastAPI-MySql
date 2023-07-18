from fastapi import APIRouter
from config.db import connection
from models.user import users
from schemas.user import User

router = APIRouter(prefix='/api/user', tags=['User'])


@router.get('/')
async def get_users():
    all_users = []
    response = connection.execute(users.select()).fetchall()
    for doc in response:
        user = (dict(zip(users.columns.keys(), doc)))
        all_users.append(user)
    return all_users


@router.get('/{id}')
async def get_user(id: str):
    result = connection.execute(
        users.select().where(users.c.id == id)).first()
    return dict(zip(users.columns.keys(), result))


@router.put('/{id}')
async def update_user(id: str):
    return 'Buenas desde router'


@router.delete('/{id}')
async def delete_user(id: str):
    return 'Buenas desde router'
