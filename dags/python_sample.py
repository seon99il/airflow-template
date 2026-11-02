from datetime import datetime

from airflow.sdk import DAG
from openlineage.client.event_v2 import Dataset

from dataplatform.operators.domain import PythonDockerOperator

POLARIS_ENV = {
    "POLARIS_URI": "http://polaris:8181/api/catalog",
    "POLARIS_CREDENTIAL": "root:s3cr3t",
    "S3_ENDPOINT": "http://rustfs:9000",
    "S3_ACCESS_KEY": "rustfs",
    "S3_SECRET_KEY": "rustfs123",
}

NUMBERS = Dataset(namespace="s3://warehouse", name="sample/numbers")

with DAG("python_sample", schedule=None, start_date=datetime(2025, 1, 1), catchup=False):
    hello = PythonDockerOperator(
        task_id="hello_world",
        file="hello.py",
        func="world",
    )
    write = PythonDockerOperator(
        task_id="write_iceberg",
        file="iceberg_sample.py",
        func="write",
        outlets=[NUMBERS],
        network_mode="airflow-template_default",
        environment=POLARIS_ENV,
    )
    read = PythonDockerOperator(
        task_id="read_iceberg",
        file="iceberg_sample.py",
        func="read",
        inlets=[NUMBERS],
        network_mode="airflow-template_default",
        environment=POLARIS_ENV,
    )
    hello >> write >> read
