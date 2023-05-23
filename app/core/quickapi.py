# app/quickapi/core/quickapi.py
from typing import Any, Dict, List, Tuple, Type

from app.core.database import db, Base
from app.core.query import Pagination, get_records, get_record, create_record, QueryParameters

from app.util.utils import transform_response, row2dict


class QueryHandler:
    def __init__(self, table: Type[Base]):
        self.table = table

    async def find_records(self, query_parameters: QueryParameters) -> Tuple[List[Any], Pagination]:
        # Fetch records from the database using sanitized_query_params
        async with db.get_session() as session:
            records, pagination = await get_records(
                session,
                self.table,
                sort=query_parameters.sort,
                filters=query_parameters.filters,
                populate=query_parameters.populate,
                fields=query_parameters.fields,
                pagination=query_parameters.pagination
            )
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
        query_handler = self.query(table)
        records, pagination = await query_handler.find_records(query_parameters)
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
