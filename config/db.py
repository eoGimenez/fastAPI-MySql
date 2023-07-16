import os
from sqlalchemy import create_engine, MetaData

user_sql = os.environ.get("USER_SQL")
password_sql = os.environ.get("PASSWORD_SQL")
port_sql = os.environ.get("PORT_SQL")
db_sql = os.environ.get("DB_SQL")

engine = create_engine(f"mysql+pymysql://{user_sql}:{password_sql}:{port_sql}/{db_sql}")

connection = engine.connect()
