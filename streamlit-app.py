import os

import pandas
import streamlit

import plotly.express as px

from sqlalchemy import create_engine

from valometa.data import sqlite_db_path
from valometa.utils.data import get_matches_per_day

uploaded_data_path = f"{os.path.dirname(__file__)}/uploaded_data"


@streamlit.cache
def get_data(sqlite_path: str = None) -> pandas.DataFrame:
    if sqlite_path:
        engine = create_engine(f"sqlite:///{sqlite_path}")
    else:
        engine = create_engine("sqlite:///vlr-gg.db")

    return pandas.read_sql_table("matches", con=engine)


database_path = sqlite_db_path

streamlit.title("Valorant Agent Meta Analyzer")

uploaded_file = streamlit.file_uploader(
    "Choose an sqlite DB to upload", accept_multiple_files=False
)

if uploaded_file:
    database_path = f"{uploaded_data_path}/temp.db"
    with open(database_path, "wb") as f:
        f.write(uploaded_file.getvalue())

match_data = get_data(database_path)

match_count_per_day = get_matches_per_day(match_data)

streamlit.markdown("## Valorant matches scraped from vlr.gg")
streamlit.dataframe(match_data)

streamlit.markdown("## Valorant matches per day")
streamlit.dataframe(match_count_per_day)

minimum_date = match_count_per_day.timestamp.min()
maximum_date = match_count_per_day.timestamp.max()

date_range = streamlit.slider(
    "Select date range",
    value=(minimum_date, maximum_date),
    min_value=minimum_date,
    max_value=maximum_date
)

filtered_match_counts = (
    match_count_per_day
    .query("timestamp >= @date_range[0] and timestamp <= @date_range[1]")
    .assign(color='#eeeeee')
)

p = px.line(filtered_match_counts, x='timestamp', y='count')

# find better way to fix line colors - this is stupid
p.data[0].line.color = "#eeeeee"

streamlit.plotly_chart(p, use_container_width=True)

agent_list = ['Astra', 'Jett', 'Omen', 'Yoru']

options = streamlit.multiselect(
     'What agents do you want to see?',
     agent_list, agent_list
)

streamlit.write('You selected:', options)