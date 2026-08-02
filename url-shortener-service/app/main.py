from fastapi import FastAPI

from app.core.lifespan import lifespan

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def hello():
    return {"message": "Welcome to url-shortener"}
