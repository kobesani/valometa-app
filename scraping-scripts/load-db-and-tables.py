#! /usr/bin/env python3

import argparse

import pandas

from sqlalchemy import create_engine

from valometa.data import sqlite_db_path

if __name__ == "__main__":

    desc = """
        Load tables into pandas dataframes from sqlite database
    """

    parser = argparse.ArgumentParser(
        prog='load-db-and-tables.py', description=desc
    )

    parser.add_argument(
        "--sqlite-path", type=str, required=False, default=sqlite_db_path,
        help="Path to sqlite database for wine reviews dumps"
    )

    parser.add_argument(
        '--table-names', type=str, nargs='+', required=False, default = [],
        help="Names of tables to load from sqlite db"
    )

    args = parser.parse_args()

    engine = create_engine(f"sqlite:///{args.sqlite_path}")

    # inspect, get table names, check args!

    tables = {
        x: pandas.read_sql_table(x, con=engine) for x in args.table_names
    }

