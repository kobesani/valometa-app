from airflow import settings
from airflow.models import Connection

from loguru import logger

from valometa.data import sqlite_db_path

connections = {
    "valometa-vlr-gg": {
        "conn_type": "sqlite",
        "description": None,
        "host": sqlite_db_path,
        "login": None,
        "password": None,
        "schema": None,
        "port": None,
        "extra": None
    }
}

connection_id = 'valometa-vlr-gg'

session = settings.Session()

connections_found = (
    session
    .query(Connection)
    .filter(Connection.conn_id == connection_id)
)

num_connections = connections_found.count()

if num_connections == 1:
    connection_id_found = connections_found.first().conn_id
    logger.info(
        f"{num_connections} connection found: {connection_id_found}"
    )

connections_found.delete()
session.commit()

logger.info(f"Old {connection_id_found} deleted")

conn = Connection(
        conn_id=connection_id,
        conn_type='sqlite',
        description=None,
        extra=None,
        host=sqlite_db_path,
        login=None,
        password=None,
        port=None,
        schema=None
)

session.add(conn)
session.commit()

logger.info(f"New {connection_id} added")
