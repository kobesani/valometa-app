import pandas

from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine

from valometa.api import templates_path
from valometa.api.schemas import NumberMatchesDay
from valometa.data import sqlite_db_path
from valometa.utils.data import get_matches_per_day


app = FastAPI(title="Valometa App")
templates = Jinja2Templates(directory=templates_path)


@app.get("/", response_class=FileResponse)
def root():
    return FileResponse(
        f"{templates_path}/base.html", media_type="text/html"
    )


@app.post("/valometa/matches-per-day", response_class=templates.TemplateResponse)
def matches_per_day_endpoint(
    request: Request,
    begin: str = Form(...),
    end: str = Form(...)
) -> templates.TemplateResponse:

    engine = create_engine(f"sqlite:///{sqlite_db_path}")

    matches_df = (
        pandas
        .read_sql_table("matches", con=engine)
        .query("timestamp >= @begin")
        .query("timestamp <= @end")
    )

    matches_per_day_df = get_matches_per_day(matches_df)

    matches_per_day_list = [
        NumberMatchesDay(date_of_count=res['timestamp'], count=res['count'])
        for _, res in matches_per_day_df.iterrows()
    ]

    return templates.TemplateResponse(
        'table.html', {'request': request, 'data': matches_per_day_list}
    )
