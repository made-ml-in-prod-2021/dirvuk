from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago
from airflow.sensors.filesystem import FileSensor

from datetime import datetime
from utils import default_args, VOLUME_DIR

with DAG (
        "train_models",
        default_args=default_args,
        schedule_interval="@weekly",
        start_date=datetime.now ()
) as dag:
    start_task = DummyOperator (task_id='start-train-pipeline')

    data_await = FileSensor (
        task_id="await-features",
        poke_interval=10,
        retries=100,
        filepath="data/raw/{{ ds }}/data.csv"
    )
    target_await = FileSensor (
        task_id="await-target",
        poke_interval=10,
        retries=100,
        filepath="data/raw/{{ ds }}/target.csv"
    )

    preprocess = DockerOperator (
        image="airflow-train",
        command="--input_dir data/raw/{{ ds }} "
                "--output_dir data/processed/{{ ds }}",
        do_xcom_push=False,
        task_id="data-preprocess",
        volumes=[f"{VOLUME_DIR}:/data"],
        entrypoint="python preprocess.py"
    )

    split = DockerOperator (
        task_id="split-data",
        image="airflow-train",
        command="--input_dir /data/raw/{{ ds }}",
        do_xcom_push=False,
        volumes=[f"{VOLUME_DIR}:/data"],
        entrypoint="python split.py"
    )

    train = DockerOperator (
        task_id="train-model",
        image="airflow-train",
        command="--input_dir /data/raw/{{ ds }} --model_dir /data/models/{{ ds }}",
        do_xcom_push=False,
        volumes=[f"{VOLUME_DIR}:/data"],
        entrypoint="python train.py"
    )
    validate = DockerOperator (
        task_id="evaluate-model",
        image="airflow-train",
        command="--input_dir /data/raw/{{ ds }} --model_dir /data/models/{{ ds }}",
        do_xcom_push=False,
        volumes=[f"{VOLUME_DIR}:/data"],
        entrypoint="python validate.py"
    )
    end_task = DummyOperator (task_id='end-train-pipeline')

    start_task >> [data_await, target_await] >> preprocess >> split >> train >> validate >> end_task
