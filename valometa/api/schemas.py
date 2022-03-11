from datetime import date

from pydantic import BaseModel


class DateRange(BaseModel):
    date_begin: date
    date_end: date


class NumberMatchesDay(BaseModel):
    date_of_count: date
    count: int


class MapPatchFilter(BaseModel):
    map_name: str
    patch: str