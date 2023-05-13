#app/quickapi/core/response_model.py
from typing import Generic, TypeVar, Optional

from fastapi import HTTPException
from pydantic.generics import GenericModel

DataT = TypeVar('DataT')


class ResponseModelStatus(GenericModel, Generic[DataT]):
    status: bool
    message: str
    data: Optional[DataT]


class CustomException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)
        self.status_code = status_code
        self.detail = detail


