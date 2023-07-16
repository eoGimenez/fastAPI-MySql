import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from fastapi import APIRouter, Security, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from passlib.context import CryptContext
from config.db import connection
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


auth_handler = AuthHandler()


@router.post('/signup', status_code=201)
async def create_user(user_details: User):

    if connection.execute(users.select().where(users.c.email == user_details.email)).first():
        raise HTTPException(
            400, 'Ya existe ese usuario. ¿ Has olvidado tu contraseña ?')
    hashed_pass = auth_handler.get_password_hash(user_details.password)
    new_user = user_details.model_dump()
    new_user['password'] = hashed_pass
    print(new_user)
    return 'testeando'
