from typing import Any, Dict, List

from app.core.query import Pagination
from app.core.security import has_permission
from fastapi import Request


def sanitize_query(query: Dict[str, Any]) -> Dict[str, Any]:
    sanitized_query = {}

    # Sort
    if "sort" in query:
        sanitized_query["sort"] = query["sort"]

    # Filters
    filter_operators = [
        "$eq", "$eqi", "$ne", "$lt", "$lte", "$gt", "$gte", "$in", "$notIn",
        "$contains", "$notContains", "$containsi", "$notContainsi", "$null", "$notNull",
        "$between", "$startsWith", "$startsWithi", "$endsWith", "$endsWithi",
        "$or", "$and", "$not"
    ]
    filters = {}
    for key, value in query.items():
        if key.startswith("filters"):
            field, operator = key.split("[")[1].split("]")
            if operator in filter_operators:
                filters[field] = {operator: value}
    if filters:
        sanitized_query["filters"] = filters

    # Populate
    if "populate" in query:
        sanitized_query["populate"] = query["populate"]

    # Fields
    if "fields" in query:
        sanitized_query["fields"] = query["fields"]

    # Pagination
    pagination_data = {
        "page": int(query.get("page", 1)),
        "page_size": int(query.get("pageSize", 10)),
        "with_count": bool(query.get("withCount", True))
    }
    sanitized_query["pagination"] = Pagination(**pagination_data)

    return sanitized_query


def row2dict(row):
    return {column.name: getattr(row, column.name) for column in row.__table__.columns}


def row2dict(row):
    if not row:
        return {}
    if hasattr(row, "_asdict"):
        return row._asdict()
    return {column.name: getattr(row, column.name) for column in row.__table__.columns}


def transform_response(records: List[Any], pagination: Dict[str, Any]) -> Dict[str, Any]:
    records_list = [row2dict(r) for r in records]
    response = {
        "data": records_list,
        "pagination": pagination
    }

    return response


def name_prefix(prefix):
    def decorator(func):
        func.__name__ = f"{prefix}:{func.__name__}"
        return func

    return decorator

