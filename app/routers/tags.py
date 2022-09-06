from fastapi import APIRouter

router = APIRouter(
    prefix="/tags",
    tags=["tags"]
)

@router.get("/")
def read_tags():
    return { "message" : "Hello World" }