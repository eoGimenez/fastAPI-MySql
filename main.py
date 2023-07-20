from fastapi import FastAPI
from routes import user, auth, post

app = FastAPI(
    title="API de map-RECS",
    description="Aqui encontraras todos los end-points de la app map-RECS",
    version="0.0.1"
)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(post.router)


@app.get('/')
async def root():
    return 'welcome'
