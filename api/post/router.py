from fastapi import APIRouter

router = APIRouter()

@router.get("/posts", tags=["posts"])
async def find():
    return []

@router.get("/posts/{id}/", tags=["posts"])
async def findOne(id: int):
    return {}

@router.post("/posts", tags=["posts"])
async def create():
    return {}

@router.put("/posts/{id}", tags=["posts"])
async def update(id: int):
    return {}

@router.delete("/posts/{id}", tags=["posts"])
async def delete(id: int):
    return {}
