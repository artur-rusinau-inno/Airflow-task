from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.sdk import dag


@dag
def snowflake():

    run_a_query = SQLExecuteQueryOperator(
        task_id="run_a_query", sql="SELECT 1 FROM table1", conn_id="snowflake"
    )
