import pandas

from typing import List

from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine

from valometa.api import templates_path
from valometa.api.schemas import (
    AgentPickCount,
    AllAgentPicks,
    DateRange,
    NumberMatchesDay,
    MapPatchFilter
)
from valometa.data import sqlite_db_path
from valometa.data.raw import valorant_patches_table
from valometa.utils.data import (
    get_matches_per_day, get_agent_pick_rates
)

app = FastAPI(title="Valometa App")
templates = Jinja2Templates(directory=templates_path)

app.mount(
    "/static", StaticFiles(directory=templates_path), name="static"
)


@app.get("/", response_class=FileResponse)
def root():
    return FileResponse(
        f"{templates_path}/base.html", media_type="text/html"
    )


@app.post("/valometa/matches-per-day", response_class=HTMLResponse)
def matches_per_day_endpoint(
    request: Request,
    begin: str = Form(...),
    end: str = Form(...)
) -> templates.TemplateResponse:

    engine = create_engine(f"sqlite:///{sqlite_db_path}")

    matches_df = (
        pandas
        .read_sql_table("matches", con=engine)
        .query(f"timestamp >= {begin}")
        .query(f"timestamp <= {end}")
    )

    matches_per_day_df = get_matches_per_day(matches_df)

    matches_per_day_list = [
        NumberMatchesDay(
            date_of_count=res['timestamp'], count=res['count']
        ) for _, res in matches_per_day_df.iterrows()
    ]

    return templates.TemplateResponse(
        'table.html', {
            'request': request, 'data': matches_per_day_list
        }
    )


@app.post(
    "/valometa/matches-per-day-json",
    response_model=List[NumberMatchesDay]
)
def matches_per_day_json_endpoint(date_range: DateRange):
    engine = create_engine(f"sqlite:///{sqlite_db_path}")

    matches_df = (
        pandas
        .read_sql_table("matches", con=engine)
        .query("timestamp >= @date_range.date_begin")
        .query("timestamp <= @date_range.date_end")
    )

    matches_per_day_df = get_matches_per_day(matches_df)

    return [
        NumberMatchesDay(
            date_of_count=res['timestamp'], count=res['count']
        ) for _, res in matches_per_day_df.iterrows()
    ]


@app.post(
    "/valometa/agents-map-patch-rate",
    response_model=AllAgentPicks
)
def agents_per_map_per_patch(picks_filter: MapPatchFilter):
    engine = create_engine(f"sqlite:///{sqlite_db_path}")

    agent_pick_rates = get_agent_pick_rates(
        pandas.read_sql('agents', con=engine),
        picks_filter.patch_lower,
        picks_filter.patch_upper,
        map_name=picks_filter.map_name
    )

    selected_patches = (
        valorant_patches_table
        .query("Patch >= @picks_filter.patch_lower")
        .query("Patch <= @picks_filter.patch_upper")
        .Patch
        .to_list()
    )

    return AllAgentPicks(
        map_name=picks_filter.map_name,
        patches=selected_patches,
        pick_rates=[
            AgentPickCount(
                agent_name=row.agent_name, pick_count=row.pick_rate
            ) for _, row in agent_pick_rates.iterrows()
        ]
    )
