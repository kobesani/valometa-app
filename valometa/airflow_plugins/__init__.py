from airflow import DAG

from airflow.operators import sqlite_operator

sqlite_conn_id = 'valometa-vlr-gg'

# valometa_dag = DAG(
#     'test-valometa',
#     default_args={}
# )

# create_tables_task = sqlite_operator(
#     task_id="create_tables",
#     dag=valometa_dag,
#     sql="create_tables.sql",
#     sqlite_conn_id="valometa-vlr-gg"
# )

