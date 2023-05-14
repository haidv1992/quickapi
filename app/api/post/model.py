# api/post/model.py
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List

from pydantic import BaseModel
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from app.core.query import FilterOperators, Pagination
from app.api.post.db import Post


class PostCreate(sqlalchemy_to_pydantic(Post, exclude=['id', 'created_at', 'updated_at'])):
    class Config:
        orm_mode = True

    def dict(self, **kwargs) -> Dict[str, Any]:
        result = super().dict(**kwargs)
        for key, value in result.items():
            if isinstance(value, datetime):
                result[key] = value.astimezone(timezone.utc).replace(tzinfo=None)
        return result


PostResponse = sqlalchemy_to_pydantic(Post)

PostUpdateRequest = sqlalchemy_to_pydantic(Post, exclude=['created_at', 'updated_at'])


class FindPostsRequest(BaseModel):
    sort: Optional[List[str]]
    filters: Optional[FilterOperators]
    populate: Optional[List[str]]
    fields: Optional[List[str]]
    pagination: Pagination = Pagination()


class FindPostsResponse(BaseModel):
    records: List[PostResponse]
    pagination: Pagination
