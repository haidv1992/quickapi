# app/api/post/router.py
from typing import List

from fastapi import APIRouter, Depends

from app.core.security import ResponseModelStatus, has_permission
from app.core.query import QueryParameters
from app.api.post.controller import (
    find_posts,
    find_post,
    create_post,
    update_post,
    delete_post,
    create_bulk_post,
)
from app.api.post.model import PostCreate, PostResponse

# Group 1: Items
from app.util.utils import name_prefix

posts_router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    dependencies=[Depends(has_permission)],
    responses={404: {"description": "Not found"}},
)


@posts_router.get("/")
@name_prefix("posts")
async def find(query_parameters: QueryParameters = Depends()):
    return 1
    return await find_posts(query_parameters)


@posts_router.get("/{id}/", response_model=PostResponse)
@name_prefix("posts")
async def findOne(id: int):
    return await find_post(id)


@posts_router.post("/", response_model=PostResponse)
@name_prefix("posts")
async def create(item: PostCreate):
    return await create_post(item.dict())


@posts_router.post("/bulk", response_model=List[PostResponse])
@name_prefix("posts")
async def createBulk(items: List[PostCreate]):
    return await create_bulk_post(items.dict())


@posts_router.patch("/{id}", response_model=PostResponse)
@name_prefix("posts")
async def update(id: int):
    return await update_post(id)


@posts_router.delete("/{id}", response_model=ResponseModelStatus)
@name_prefix("posts")
async def delete(id: int):
    return await delete_post(id)

routers = [posts_router]
