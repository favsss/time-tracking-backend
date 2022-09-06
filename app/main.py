from tabnanny import check
from fastapi import FastAPI
from .routers import tags, users, token, checkins

app = FastAPI()

app.include_router(tags.router)
app.include_router(users.router)
app.include_router(token.router)
app.include_router(checkins.router)

@app.get("/")
def root():
    return { "message" : "Hello World" }