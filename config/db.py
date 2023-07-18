import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

load_dotenv()

user_sql = os.environ.get("USER_SQL")
password_sql = os.environ.get("PASSWORD_SQL")


engine = create_engine(
    f'mysql+pymysql://{user_sql}:{password_sql}@localhost:3306/testeando')

SessionLocal = sessionmaker(engine)

meta = MetaData()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
