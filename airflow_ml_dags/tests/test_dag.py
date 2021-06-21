import sys

import pytest
from airflow.models import DagBag


sys.path.append("dags")


@pytest.fixture()
def dags_airflow():
    """Загружаем DAG."""
    return DagBag(dag_folder="dags/", include_examples=False)


def test_dags_airflow_import_correct(dags_airflow):
    assert dags_airflow.dags is not None
    assert dags_airflow.import_errors == {}


def test_generation_data_dag_load(dags_airflow):
    assert "download_data" in dags_airflow.dags
    assert len(dags_airflow.dags["download_data"].tasks) == 3


def test_generation_data_dag_structure(dags_airflow):
    generation_structure = {
        "start-download-data": ["docker-airflow-download"],
        "docker-airflow-download": ["end-download-data"],
        "end-download-data": [],
    }
    dag = dags_airflow.dags["download_data"]
    for name, task in dag.task_dict.items():
        assert set(generation_structure[name]) == task.downstream_task_ids


def test_train_model_dag_load(dags_airflow):
    assert "train_models" in dags_airflow.dags
    assert len(dags_airflow.dags["train_models"].tasks) == 8


def test_train_model_dag_structure(dags_airflow):
    structure_train = {
        "start-train-pipeline": ["await-target", "await-features"],
        "await-features": ["data-preprocess"],
        "await-target": ["data-preprocess"],
        "data-preprocess": ["split-data"],
        "split-data": ["train-model"],
        "train-model": ["evaluate-model"],
        "evaluate-model": ["end-train-pipeline"],
        "end-train-pipeline": [],
    }
    dag = dags_airflow.dags["train_models"]
    for name, task in dag.task_dict.items():
        assert set(structure_train[name]) == task.downstream_task_ids


def test_predicts_dag_load(dags_airflow):
    assert "make_predict" in dags_airflow.dags
    assert len(dags_airflow.dags["make_predict"].tasks) == 5


def test_predicts_dag_structure(dags_airflow):
    structure_predict = {
        "start-predict": ["data_wait", "model_wait"],
        "data_wait": ["predict"],
        "model_wait": ["predict"],
        "predict": ["end-predict"],
        "end-predict": [],
    }
    dag = dags_airflow.dags["make_predict"]
    for name, task in dag.task_dict.items():
        assert set(structure_predict[name]) == task.downstream_task_ids

