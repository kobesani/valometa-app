from airflow import DAG

from airflow.operators import sqlite_operator

# from valometa.airflow_plugins.operators import LoadMatchesOperator

from airflow_plugins.operators import LoadMatchesOperator

sqlite_conn_id = 'valometa-vlr-gg'

valometa_dag = DAG(
    'test-valometa',
    default_args={}
)

create_tables_task = sqlite_operator(
    task_id="create_tables",
    dag=valometa_dag,
    sql="create_tables.sql",
    sqlite_conn_id=sqlite_conn_id
)

populate_tables_task = LoadMatchesOperator(
    task_id="load_matches",
    dag=valometa_dag,
    sqlite_conn_id=sqlite_conn_id
)

create_tables_task >> populate_tables_task
