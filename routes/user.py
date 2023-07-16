from fastapi import APIRouter
from config.db import connection
from models.user import users
from schemas.user import User

router = APIRouter(prefix='/api/user', tags=['User'])


@router.get('/')
async def get_users():
    return connection.execute(users.select()).fetchall()


@router.get('/{id}')
async def get_user(id: str):
    return 'Buenas desde router'


@router.post('/')
async def create_user(user_details: User):
    # new_user = connection.execute(users.select()).fetchone()
    new_user = user_details.model_dump()
    print(new)
    return 'Buenas desde router'


@router.put('/{id}')
async def update_user(id: str):
    return 'Buenas desde router'


@router.delete('/{id}')
async def delete_user(id: str):
    return 'Buenas desde router'
