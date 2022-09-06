from fastapi import FastAPI
from .routers import tags

app = FastAPI()

app.include_router(tags.router)

@app.get("/")
def root():
    return { "message" : "Hello World" }