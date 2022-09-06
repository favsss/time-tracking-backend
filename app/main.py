from fastapi import FastAPI
from .routers import tags, users

app = FastAPI()

app.include_router(tags.router)
app.include_router(users.router)

@app.get("/")
def root():
    return { "message" : "Hello World" }