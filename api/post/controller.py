from typing import Any,Dict

from api.post.db import Post
from app.quickapi.core.quickapi import QuickAPI

qa = QuickAPI()


async def find_posts(query_parameters):
    return await qa.find(table=Post, query_parameters=query_parameters)


async def find_post(id: int):
    response = await qa.findOne(table=Post, id=id)
    return response


async def create_post(item: Dict[str, Any]):
    response = await qa.create(table=Post, item=item)
    return response

async def create_bulk_post(items: Dict[str, Any]):
    response = await qa.createBulk(table=Post, items=items)
    return response


async def update_post(id: int):
    return {}


async def delete_post(id: int):
    return {}
