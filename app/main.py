from tabnanny import check
from fastapi import FastAPI
from .routers import tags, users, token, checkins
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(tags.router)
app.include_router(users.router)
app.include_router(token.router)
app.include_router(checkins.router)

@app.get("/")
def root():
    return { "message" : "Hello World" }