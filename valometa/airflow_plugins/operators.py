import enum
import os

import pandas
import parsel
import pendulum
import requests

from airflow.models import BaseOperator
from airflow.providers.sqlite.hooks.sqlite import SqliteHook

from valometa.airflow_plugins import sqlite_conn_id

from valometa.extractors.results.selectors import CardExtractor
from valometa.extractors.results.other import DateExtractor

class LoadMatchesOperator(BaseOperator):
    def __init__(
        self,
        sqlite_conn_id: str = sqlite_conn_id,
        *args,
        **kwargs
    ) -> None:

        super(LoadMatchesOperator, self).__init__(*args, **kwargs)
        self.sqlite_conn_id = sqlite_conn_id
        self.output_table = 'matches'

    def clean_up(self, sqlite_hook: SqliteHook):
        self.log.info(f"Cleanup procedure for matches table ...")

        delete_sql = f"DELETE FROM {self.output_table}"
        sqlite_hook.run(delete_sql)

    def populate_matches_table(
        self, sqlite_hook: SqliteHook, data: pandas.DataFrame
    ):
        nrecords = len(data)
        self.log.info(
            f"Populating matches table with {nrecords} records ... "
        )

        try:
            engine = sqlite_hook.get_sqlalchemy_engine()
            conn = engine.connect()
            data.to_sql(
                name=self.output_table,
                con=conn,
                if_exists="append",
                index=False,
                chunksize=10000,
                method="multi",
            )
        except Exception as error:
            self.log.error("An exception has occured: {}".format(str(error)))

    def execute(self, context):
        self.log.info("Fetching data from Kraken API: Trades endpoint...")

        data = pandas.read_csv(
            f"{os.path.dirname(__file__)}/matches.csv"
        )

        sqlite_hook = SqliteHook(sqlite_conn_id=sqlite_conn_id)
        self.clean_up(sqlite_hook)

        self.populate_matches_table(sqlite_hook, data)


def get_max_pages():
    response = requests.get(f"https://www.vlr.gg/matches/results")

    main_select = parsel.Selector(response.text)
    pages_as_str = (
        main_select
        .xpath("//a[@class='btn mod-page']")
        .xpath("./text()")[-1]
        .get()
    )

    return int(pages_as_str)


def match_card_extractor(days_in_past: int):
    max_pages = get_max_pages()

    extraction_date = (
        pendulum
        .now()
        .subtract(days=days_in_past)
        .date()
        .format("ddd, MMMM DD, YYYY")
    )

    cards_dict = {}
    for page in range(1, max_pages + 1):
        response = requests.get(
            f"https://www.vlr.gg/matches/results/?page={page}"
        )

        main_select = parsel.Selector(response.text)

        dates = list(DateExtractor(main_select).yield_data())
        cards = list(CardExtractor(main_select).yield_data())

        for idx, (date, card) in enumerate(zip(dates, cards)):
            if date == extraction_date:
                cards_dict[page] = card
                break
            
        # check if last index, could be more matches on next page
        if idx == (len(dates) - 1):
            continue
