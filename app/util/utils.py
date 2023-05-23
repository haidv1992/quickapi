from typing import Any, Dict, List

from fastapi import Request, APIRouter


def parse_populate_dict(populate_dict: Dict[str, Any]) -> List[str]:
    populate_list = []
    for key, value in populate_dict.items():
        if isinstance(value, dict):
            sub_populate = parse_populate_dict(value)
            sub_populate_list = [f"{key}.{sub_field}" for sub_field in sub_populate]
            populate_list.extend(sub_populate_list)
        elif value:
            populate_list.append(key)
    return populate_list

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


class PrefixedAPIRouter(APIRouter):
    def __init__(self, *args, name_prefix=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.name_prefix = name_prefix

    def add_api_route(self, *args, **kwargs):
        if self.name_prefix:
            if 'name' in kwargs and kwargs['name'] is not None:
                kwargs['name'] = f"{self.name_prefix}:{kwargs['name']}"
            else:
                kwargs['name'] = f"{self.name_prefix}:{args[1].__name__}"
        super().add_api_route(*args, **kwargs)




