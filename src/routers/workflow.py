from fastapi import APIRouter

router = APIRouter(
    prefix="", tags=["app"], responses={404: {"message": "Not found"}}
)

@router.get("/", tags=["root"])
async def root():
    return {"message": "Hello World"}
