from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.sql.sqltypes import String
from config.db import meta, engine

users = Table("users", meta,
              Column("id", String(55), primary_key=True),
              Column("name", String(55)),
              Column("email", String(255)),
              Column("password", String(255))
              )


meta.create_all(engine)
