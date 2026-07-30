from fastapi import Depends, FastAPI

app = FastAPI()

@app.get("/")
async def hello():
    return { "message": "Welcome to url-shortener" }