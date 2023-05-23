# app/api/post/router.py
import re
from typing import List
from urllib.parse import parse_qs, unquote_plus, parse_qsl

from fastapi import  Depends,Request

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

from app.util.utils import PrefixedAPIRouter

# Group 1: Items
posts_router = PrefixedAPIRouter(
    prefix="/posts",
    tags=["posts"],
    dependencies=[Depends(has_permission)],
    responses={404: {"description": "Not found"}},
    name_prefix="posts"
)

@posts_router.get("/")
async def find(query_parameters: QueryParameters = Depends(QueryParameters.from_request)):
    # return {"query_parameters": query_parameters}
    return await find_posts(query_parameters)

@posts_router.get("/{id}/", response_model=PostResponse)
async def findOne(id: int):
    return await find_post(id)


@posts_router.post("/", response_model=PostResponse)
async def create(item: PostCreate):
    return await create_post(item.dict())


@posts_router.post("/bulk", response_model=List[PostResponse])
async def createBulk(items: List[PostCreate]):
    return await create_bulk_post(items.dict())


@posts_router.patch("/{id}", response_model=PostResponse)
async def update(id: int):
    return await update_post(id)


@posts_router.delete("/{id}", response_model=ResponseModelStatus)
async def delete(id: int):
    return await delete_post(id)

routers = [posts_router]
