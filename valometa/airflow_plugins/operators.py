import os

import pandas

from airflow.models import BaseOperator
from airflow.providers.sqlite.hooks.sqlite import SqliteHook

from valometa.airflow_plugins import sqlite_conn_id

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