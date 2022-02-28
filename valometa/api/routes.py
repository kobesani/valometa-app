import pandas
import requests

from typing import List

from fastapi import FastAPI, Form
from fastapi.middleware.wsgi import WSGIMiddleware
from flask import Flask, render_template
from sqlalchemy import create_engine

from valometa.api.schemas import DateRange, NumberMatchesDay
from valometa.data import sqlite_db_path
from valometa.utils.data import get_matches_per_day


api_app = FastAPI()
flask_app = Flask(__name__)

app = FastAPI(title="App Root")

app.mount("/api", api_app)
app.mount("/", WSGIMiddleware(flask_app))


@flask_app.get("/")
def hello():
    # return 'Hello, World!'
    return render_template('base.html')


@api_app.post("/matches-per-day", response_model=List[NumberMatchesDay])
# def matches_per_day(date_range: DateRange) -> List[NumberMatchesDay]:
def matches_per_data(
    begin: str = Form(...),
    end: str = Form(...)
) -> List[NumberMatchesDay]:

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
