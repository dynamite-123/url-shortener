from fastapi import FastAPI
from app.api.routers import url

from app.core.lifespan import lifespan

app = FastAPI(lifespan=lifespan)

app.include_router(url.router)

@app.get("/")
async def hello():
    return {"message": "Welcome to url-shortener"}
