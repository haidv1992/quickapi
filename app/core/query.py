# app/quickapi/core/query.py
import re
from typing import List, Optional, Any, Dict, Type
from urllib.parse import parse_qs, parse_qsl, unquote_plus

from pydantic.fields import FieldInfo
from sqlalchemy import and_, desc, asc, update, delete
from pydantic import BaseModel, Field, root_validator
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session, joinedload
from fastapi import Depends, Query ,Request
import sqlalchemy as sa

from app.core.database import Base


class Pagination(BaseModel):
    page: Optional[int] = 1
    page_size: Optional[int] = 10
    with_count: Optional[bool] = True


class FilterOperators(BaseModel):
    eq: Optional[str]
    eqi: Optional[str]
    ne: Optional[str]
    lt: Optional[str]
    lte: Optional[str]
    gt: Optional[str]
    gte: Optional[str]
    in_: Optional[List[str]] = {"alias": "in"}
    notIn: Optional[List[str]]
    contains: Optional[str]
    notContains: Optional[str]
    containsi: Optional[str]
    notContainsi: Optional[str]
    is_null: Optional[bool] = {"alias": "null"}
    notNull: Optional[bool]
    between: Optional[List[str]]
    startsWith: Optional[str]
    startsWithi: Optional[str]
    endsWith: Optional[str]
    endsWithi: Optional[str]
    or_: Optional[List[str]] = {"alias": "or"}
    and_: Optional[List[str]] = {"alias": "and"}
    not_: Optional[List[str]] = {"alias": "not"}

class QueryParameters(BaseModel):
    sort: Optional[List[str]] = Field(default=["created_at"], example="created_at")
    filters: Optional[Dict[str, Any]] = None
    populate: Optional[List[str]] = None
    fields: Optional[List[str]] = None
    pagination: Pagination = Pagination()

    @classmethod
    def from_request(cls, request: Request):
        query_string = dict(parse_qsl(unquote_plus(request.url.query)))
        filters = {}
        populate = []
        fields = []
        sort = []
        for key, value in query_string.items():
            if key.startswith('filters'):
                match = re.match(r'filters\[(.*?)\]\[(.*?)\]', key)
                if match:
                    field, operator = match.groups()
                    if operator is None:
                        operator = '$eq'  # Default operator
                    filters.setdefault(field, {})[operator] = value
                else:
                    # If the key doesn't match the pattern, assume it's a field with an operator of $eq
                    field = key.split('[')[1].rstrip(']')
                    filters.setdefault(field, {})['$eq'] = value
            elif key.startswith('populate'):
                populate.append(value)
            elif key.startswith('fields'):
                fields.append(value)
            elif key.startswith('sort'):
                sort += value.split(',')

        # Pagination
        pagination_data = {
            "page": int(query_string.get("page", 1)),
            "page_size": int(query_string.get("pageSize", 10)),
            "with_count": bool(query_string.get("withCount", True))
        }
        query_string['filters'] = filters
        query_string['populate'] = populate
        query_string['fields'] = fields
        query_string['sort'] = sort
        query_string['pagination'] = pagination_data
        print(query_string)
        return cls.parse_obj(query_string)

def calculate_pagination(total_records: int, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
    total_pages = (total_records + page_size - 1) // page_size

    pagination = {
        "page": page,
        "pageSize": page_size,
        "pageCount": total_pages,
        "total": total_records
    }
    return pagination


def apply_populate(query, table, populate: Optional[List[str]]):
    if populate:
        for relationship in populate:
            query = query.options(joinedload(getattr(table, relationship)))

    return query


def apply_sort(query, table, sort: Optional[List[str]]):
    if sort:
        for sort_item in sort:
            if sort_item.startswith("-"):
                query = query.order_by(desc(getattr(table, sort_item[1:])))  # Corrected line
            else:
                query = query.order_by(asc(getattr(table, sort_item)))  # Corrected line

    return query


def apply_filters(query, table, filters: Optional[List[str]]):
    if filters:
        filter_conditions = []
        for field, operators in filters.items():
            if not operators:
                continue

            field_filter_conditions = []
            for operator, value in operators.items():
                if value is None:
                    continue

                column = getattr(table, field)  # Corrected line
                if operator == "eq":
                    field_filter_conditions.append(column == value)
                elif operator == "eqi":
                    field_filter_conditions.append(column.ilike(value))
                elif operator == "ne":
                    field_filter_conditions.append(column != value)
                elif operator == "lt":
                    field_filter_conditions.append(column < value)
                elif operator == "lte":
                    field_filter_conditions.append(column <= value)
                elif operator == "gt":
                    field_filter_conditions.append(column > value)
                elif operator == "gte":
                    field_filter_conditions.append(column >= value)
                elif operator == "in":
                    field_filter_conditions.append(column.in_(value))
                elif operator == "notIn":
                    field_filter_conditions.append(column.notin_(value))
                elif operator == "contains":
                    field_filter_conditions.append(column.like(f"%{value}%"))
                elif operator == "notContains":
                    field_filter_conditions.append(column.notlike(f"%{value}%"))
                elif operator == "containsi":
                    field_filter_conditions.append(column.ilike(f"%{value}%"))
                elif operator == "notContainsi":
                    field_filter_conditions.append(column.notilike(f"%{value}%"))
                elif operator == "is_null":
                    field_filter_conditions.append(column.is_(None))
                elif operator == "notNull":
                    field_filter_conditions.append(column.isnot(None))
                elif operator == "between":
                    field_filter_conditions.append(column.between(value[0], value[1]))
                elif operator == "startsWith":
                    field_filter_conditions.append(column.like(f"{value}%"))
                elif operator == "startsWithi":
                    field_filter_conditions.append(column.ilike(f"{value}%"))
                elif operator == "endsWith":
                    field_filter_conditions.append(column.like(f"%{value}"))
                elif operator == "endsWithi":
                    field_filter_conditions.append(column.ilike(f"%{value}"))

            filter_conditions.append(and_(*field_filter_conditions))

        query = query.where(and_(*filter_conditions))

    return query


def apply_fields(query, table, fields: Optional[List[str]]):
    if fields:
        selected_columns = [getattr(table, field) for field in fields]  # Corrected line
        query = query.with_only_columns(selected_columns)

    return query


async def get_records(
        db: Session,
        table: Type[Base],
        pagination: Pagination,
        sort: Optional[List[str]] = None,
        filters: Optional[FilterOperators] = None,
        populate: Optional[List[str]] = None,
        fields: Optional[List[str]] = None,
) -> Any:
    query = select(table).offset((pagination.page - 1) * pagination.page_size).limit(pagination.page_size)
    # Apply sort
    query = apply_sort(query, table, sort)

    # Apply filters
    query = apply_filters(query, table, filters)

    # Apply fields
    query = apply_fields(query, table, fields)

    # Apply fields and populate
    query = apply_populate(query, table, populate)

    # Create count query
    count_query = query.with_only_columns(sa.func.count()).order_by(None).offset(None).limit(None)

    # Apply fields
    query = apply_fields(query, table, fields)
    query = query.offset((pagination.page - 1) * pagination.page_size).limit(pagination.page_size)

    result = await db.execute(query)
    records = result.scalars().all()

    # Get the total number of records
    count_result = await db.execute(count_query)
    total_records = count_result.scalar_one()

    pagination = calculate_pagination(total_records, page=pagination.page, page_size=pagination.page_size)

    return records, pagination


async def get_record(
        db: Session,
        table: Type[Base],
        id: int,
) -> Any:
    try:
        record = await db.get(table, id)
        return record
    except NoResultFound:
        return None


async def create_record(
        db: Session,
        table: Type[Base],
        item: Dict[str, Any]
) -> Any:
    try:
        new_record = table(**item)
        db.add(new_record)
        await db.commit()
        await db.refresh(new_record)
        return new_record
    except NoResultFound:
        return None


async def create_records(
        db: Session,
        table: Type[Base],
        items: Dict[str, Any]
) -> Any:
    try:
        for item in items:
            stmt = (
                update(table).
                where(table.c.id == item["id"]).
                values(**item)
            )
            await db.execute(stmt)
        await db.commit()
    except NoResultFound:
        return None


async def bulk_update(
        db: Session,
        table: Type[Base],
        items: Dict[str, Any]
) -> Any:
    try:
        for item in items:
            stmt = (
                update(table).
                where(table.c.id == item["id"]).
                values(**item)
            )
            await db.execute(stmt)
        await db.commit()
    except NoResultFound:
        return None


async def bulk_insert(
        db: Session,
        table: Type[Base],
        items: Dict[str, Any]
) -> Any:
    try:
        async with db.begin():
            db.add_all([table(**item) for item in items])
        await db.commit()
    except NoResultFound:
        return None


async def bulk_delete(
        db: Session,
        table: Type[Base],
        ids: Dict[str, Any]
) -> Any:
    try:
        async with db.begin():
            await db.execute(
                delete(table).where(table.c.id.in_(ids))
            )
        await db.commit()
    except NoResultFound:
        return None
