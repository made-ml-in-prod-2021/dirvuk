from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.providers.docker.operators.docker import DockerOperator

from datetime import datetime
from utils import (
    default_args, VOLUME_DIR, RAW_DIR
)

with DAG(
        "download_data",
        default_args=default_args,
        schedule_interval="@daily",
        start_date=datetime.now()
) as dag:
    start_task = DummyOperator(task_id='start-download-data')
    download_data = DockerOperator(
        task_id="docker-airflow-download",
        image="airflow-download",
        command="--output_dir /data/raw/{{ ds }}",
        do_xcom_push=False,
        volumes=[f"{VOLUME_DIR}:/data"]
    )

    end_task = DummyOperator(task_id='end-download-data')

    start_task >> download_data >> end_task
