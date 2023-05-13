from typing import Any, Dict, List

from fastapi import APIRouter, Request, Body, Depends

from app.quickapi.core.model import ResponseModelStatus
from app.quickapi.core.query import QueryParameters
from .controller import (
    find_posts,
    find_post,
    create_post,
    update_post,
    delete_post, create_bulk_post,
)
from .model import PostCreate, PostResponse

router = APIRouter()


@router.get("/posts", tags=["posts"])
async def find(query_parameters: QueryParameters = Depends()):
    return await find_posts(query_parameters)


@router.get("/posts/{id}/", tags=["posts"], response_model=PostResponse)
async def findOne(id: int):
    return await find_post(id)


@router.post("/posts", tags=["posts"], response_model=PostResponse)
async def create(item: PostCreate):
    return await create_post(item.dict())

@router.post("/posts/bulk", tags=["posts"],response_model=List[PostResponse])
async def createBulk(items: List[PostCreate]):
    return await create_bulk_post(items.dict())


@router.patch("/posts/{id}", tags=["posts"], response_model=PostResponse)
async def update(id: int):
    return await update_post(id)


@router.delete("/posts/{id}", tags=["posts"],response_model=ResponseModelStatus)
async def delete(id: int):
    return await delete_post(id)
