from airflow import DAG

from airflow.operators.sqlite_operator import SqliteOperator
import pendulum

from valometa.airflow_plugins.operators import LoadMatchesOperator

# from airflow_plugins.operators import LoadMatchesOperator

sqlite_conn_id = 'valometa-vlr-gg'

valometa_dag = DAG(
    'test-valometa',
    default_args={},
    start_date=pendulum.today()
)

# create_tables_task = SqliteOperator(
#     task_id="create_tables",
#     dag=valometa_dag,
#     sql="create_tables.sql",
#     sqlite_conn_id=sqlite_conn_id
# )

create_matches_table = SqliteOperator(
    task_id="create_matches_table",
    dag=valometa_dag,
    sql="create_matches_table.sql",
    sqlite_conn_id=sqlite_conn_id
)

create_agents_table = SqliteOperator(
    task_id="create_agents_table",
    dag=valometa_dag,
    sql="create_agents_table.sql",
    sqlite_conn_id=sqlite_conn_id
)

populate_tables_task = LoadMatchesOperator(
    task_id="load_matches",
    dag=valometa_dag,
    sqlite_conn_id=sqlite_conn_id
)

[create_matches_table, create_agents_table] >> populate_tables_task
