import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData

load_dotenv()

user_sql = os.environ.get("USER_SQL")
password_sql = os.environ.get("PASSWORD_SQL")
print(password_sql, user_sql)


engine = create_engine(
    f'mysql+pymysql://{user_sql}:{password_sql}@localhost:3306/testeando')

meta = MetaData()


connection = engine.connect()
