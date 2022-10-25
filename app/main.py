from tabnanny import check
from fastapi import FastAPI
from .routers import tags, users, token, checkins
from fastapi.middleware.cors import CORSMiddleware
# from mangum import Mangum

app = FastAPI()

origins = [
    "http://localhost:8080",
    "https://unique-mermaid-1547ba.netlify.app",
    "https://main--unique-mermaid-1547ba.netlify.app"
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

# handler = Mangum(app)


@app.get("/")
def root():
    return { "message" : "Hello World" }