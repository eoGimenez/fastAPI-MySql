from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.sql.sqltypes import String
from config.db import meta, engine

posts = Table("posts", meta,
              Column("id", String(55), primary_key=True),
              Column("place", String(255)),
              Column("comment", String(255)),
              Column("image", String(255)),
              Column("author", String(55), ForeignKey(
                  "users.id", ondelete="CASCADE"))
              )


meta.create_all(engine)
