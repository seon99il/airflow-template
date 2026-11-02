from datetime import datetime

from airflow.sdk import DAG

from dataplatform.operators.dbt import DbtDockerOperator

with DAG("dbt_sample", schedule=None, start_date=datetime(2025, 1, 1), catchup=False):
    stg = DbtDockerOperator(task_id="stg", project="sample", conn_id="postgres_default", select="stg_numbers")
    fct = DbtDockerOperator(task_id="fct", project="sample", conn_id="postgres_default", select="fct_numbers")
    stg >> fct
