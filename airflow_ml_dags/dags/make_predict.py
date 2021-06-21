import os
from datetime import datetime

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.sensors.filesystem import FileSensor

from utils import default_args, VOLUME_DIR

with DAG(
        dag_id="make_predict",
        default_args=default_args,
        schedule_interval="@daily",
        start_date=datetime.now()) as dag:

    start_task = DummyOperator(task_id='start-predict')

    data_await = FileSensor(
        task_id='data_wait',
        poke_interval=10,
        retries=100,
        filepath="data/raw/{{ ds }}/data.csv"
    )

    model_await = FileSensor(
        task_id='model_wait',
        poke_interval=10,
        retries=2,
        filepath="data/models/{{ ds }}/model.pkl"
    )

    predict = DockerOperator(
        task_id="predict",
        image="airflow-predict",
        command="--input_dir /data/raw/{{ ds }} --output_dir /data/predictions/{{ ds }} "
                " --model_path /data/models/{{ ds }}/model.pkl",
        do_xcom_push=False,
        volumes=[f"{VOLUME_DIR}:/data"]
    )

    end_task = DummyOperator(task_id='end-predict')

    start_task >> [data_await, model_await] >> predict >> end_task
