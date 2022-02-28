import pandas

from datetime import date
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine

from valometa.data import sqlite_db_path
from valometa.utils.data import get_matches_per_day


class DateRange(BaseModel):
    date_begin: date
    date_end: date


class NumberMatchesDay(BaseModel):
    date_of_count: date
    count: int


app = FastAPI()

@app.get("/")
def root():
    return {'message': 'hello world'}


@app.post("/matches-per-day")
def matches_per_day(date_range: DateRange) -> List[NumberMatchesDay]:
    engine = create_engine(f"sqlite:///{sqlite_db_path}")
    matches_df = (
        pandas
        .read_sql_table("matches", con=engine)
        .query("timestamp >= @date_range.date_begin")
        .query("timestamp <= @date_range.date_end")
    )
    matches_per_day_df = get_matches_per_day(matches_df)

    return [
        NumberMatchesDay(date_of_count=res['timestamp'], count=res['count'])
        for _, res in matches_per_day_df.iterrows()
    ]
