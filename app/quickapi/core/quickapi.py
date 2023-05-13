# app/quickapi/core/quickapi.py
from typing import Any, Dict, List, Tuple, Type

from fastapi import Request

from app.database import db, Base
from app.quickapi.core.query import Pagination, get_records, calculate_pagination, get_record, create_record, \
    QueryParameters
from app.quickapi.util.utils import sanitize_query, transform_response, row2dict


class QueryHandler:
    def __init__(self, table: Type[Base]):
        self.table = table

    async def find_records(self, sanitized_query_params: Dict[str, Any]) -> Tuple[List[Any], Pagination]:
        # Fetch records from the database using sanitized_query_params
        async with db.get_session() as session:
            records, pagination = await get_records(session, self.table, **sanitized_query_params)
        # Calculate pagination information

        return records, pagination

    async def find_one_record(self, id: int):
        async with db.get_session() as session:
            record = await get_record(session, self.table, id)
        return record

    async def create_one_record(self,  item: Dict[str, Any]):
        async with db.get_session() as session:
            record = await create_record(session, self.table, item)
        return record
    async def create_bulk_records(self,  items: Dict[str, Any]):
        async with db.get_session() as session:
            record = await create_records(session, self.table, items)
        return record


class QuickAPI:

    def query(self, table: str) -> QueryHandler:
        return QueryHandler(table)

    async def find(self, table: Type[Base], query_parameters: QueryParameters):
        print(11,query_parameters)
        sanitized_query_params = sanitize_query(query_parameters)
        query_handler = self.query(table)
        records, pagination = await query_handler.find_records(sanitized_query_params)
        response = transform_response(records=records, pagination=pagination)
        return response

    async def findOne(self, table: Type[Base], id: int):
        query_handler = self.query(table)
        record = await query_handler.find_one_record(id)
        response = row2dict(record)
        return response

    async def create(self, table: Type[Base], item: Dict[str, Any]):
        query_handler = self.query(table)
        record = await query_handler.create_one_record(item)
        response = row2dict(record)
        return response
    async def createBulk(self, table: Type[Base], items: Dict[str, Any]):
        query_handler = self.query(table)
        record = await query_handler.create_bulk_records(items)
        response = row2dict(record)
        return response
