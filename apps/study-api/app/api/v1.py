from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1",
    tags=["api v1"],
)


@router.get("/hello")
def hello_world():
    return {"message": "hello world!"}
