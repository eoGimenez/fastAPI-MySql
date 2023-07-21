from fastapi import APIRouter, Depends, HTTPException, status, Response
from starlette.status import HTTP_204_NO_CONTENT
from config.db import get_db
from models.user import users
from sqlalchemy.orm import Session
from .auth import AuthHandler
from schemas.user import User

router = APIRouter(prefix='/api/user', tags=['User'])

auth_handler = AuthHandler()


@router.get('/', response_model=list[User])
async def get_users(db: Session = Depends(get_db)):
    all_users = []
    response = db.execute(users.select()).fetchall()
    for doc in response:
        user = (dict(zip(users.columns.keys(), doc)))
        all_users.append(user)
    return all_users


@router.get('/{id}', response_model=User)
async def get_user(id: str, db: Session = Depends(get_db)):
    result = db.execute(
        users.select().where(users.c.id == id)).first()
    if (not result):
        raise HTTPException(
            404, f"El usuario con el id: '{id}', no existe en la base de datos")
    return dict(zip(users.columns.keys(), result))


@router.put('/{id}', response_model=User)
async def update_user(id: str, user_details: User, id_token=Depends(auth_handler.auth_wrapper), db: Session = Depends(get_db)):
    found_user: User = db.execute(
        users.select().where(users.c.id == id)).first()
    if (not found_user):
        raise HTTPException(
            404, f"El usuario con el id: '{id}', no existe en la base de datos")
    if (found_user.id != id_token):
        raise HTTPException(
            401, 'No puedes eliminar o modificar otros usuarios sin permisos de ADMIN')
    db.execute(
        users.update().values({"name": user_details.name,
                               "email": user_details.email}).where(users.c.id == id))
    db.commit()
    updated_user: User = dict(zip(users.columns.keys(), db.execute(
        users.select().where(users.c.id == id)).first()))
    return updated_user


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str, id_token=Depends(auth_handler.auth_wrapper), db: Session = Depends(get_db)):
    found_user: User = db.execute(
        users.select().where(users.c.id == id)).first()
    if (not found_user):
        raise HTTPException(
            404, f"El usuario con el id: '{id}', no existe en la base de datos")
    if (found_user.id != id_token):
        raise HTTPException(
            401, 'No puedes eliminar o modificar otros usuarios sin permisos de ADMIN')
    db.execute(users.delete().where(users.c.id == id))
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)
