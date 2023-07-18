import os
from datetime import datetime, timedelta
import random
import string
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Security, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from config.db import get_db
from models.user import users
from schemas.user import User

load_dotenv()

router = APIRouter(prefix='/api/auth', tags=['Auth'])


class AuthHandler():
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = os.environ.get("SECRET")

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, user_id):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=4001, detail='Ah expirado el tiempo de la firma, por favopr vuelva a conectarse')
        except jwt.InvalidTokenError as e:
            raise HTTPException(
                status_code=401, detail='Credenciales incorrectas, compruebe sus datos')

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)

    def id_generator(self):
        chars = string.ascii_letters
        digits = string.digits
        id = "".join(random.choices(f'{chars}{digits}', k=28))
        return id


auth_handler = AuthHandler()


@router.post('/signup', status_code=201)
async def create_user(user_details: User, db: Session = Depends(get_db)):
    if db.execute(users.select().where(users.c.email == user_details.email)).first():
        raise HTTPException(
            400, 'Ya existe ese usuario. ¿ Has olvidado tu contraseña ?')
    hashed_pass = auth_handler.get_password_hash(user_details.password)
    new_id = auth_handler.id_generator()
    new_user = {"id": new_id, "name": user_details.name,
                "email": user_details.email, "password": hashed_pass}
    result = db.execute(users.insert().values(new_user))
    found_user = db.execute(
        users.select().where(users.c.id == new_id)).first()
    created_user = (dict(zip(users.columns.keys(), found_user)))
    db.commit()
    return created_user


@router.post('/login', status_code=200)
async def login_user(user_details: User, db: Session = Depends(get_db)):
    result = db.execute(
        users.select().where(users.c.email == user_details.email)).first()
    user = dict(zip(users.columns.keys(), result))
    if (not user or (not auth_handler.verify_password(user_details.password, user['password']))):
        raise HTTPException(
            401, 'Credenciales incorrectas, ¿ has olvidado tu contraseña ?')
    token = auth_handler.encode_token(user['email'])
    return {"token": token}


@router.get('/verify', status_code=201)
async def verify_token(email=Depends(auth_handler.auth_wrapper), db: Session = Depends(get_db)):
    result: User = db.execute(
        users.select().where(users.c.email == email)).first()
    user_token = dict(zip(users.columns.keys(), result))
    return user_token
