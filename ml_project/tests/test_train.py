import os
import pytest

from py._path.local import LocalPath
from enities.model_params import ModelParams
from enities.split_params import SplittingParams
from train_pipeline import train_pipeline
from train_pipeline_params import TrainingPipelineParams
from faker import Faker


@pytest.fixture()
def fake_dataset_path(tmpdir):
    faker = Faker()

    tmp_file = tmpdir.mkdir("tmp").join("fake_data_sample.csv")
    head = "age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal,target\n"

    # prepare fake data
    data = ""
    for _ in range(10):
        line = []
        for _ in range(15):
            line.append(str(faker.random_int(1)))
        data += ",".join(line)
        data += "\n"
    print(data)
    tmp_file.write(head + data)
    return tmp_file


def test_train(tmpdir: LocalPath, fake_dataset_path: str):
    expected_output_model_path = os.path.join(str(tmpdir), "model.pkl")
    expected_metric_path = os.path.join(str(tmpdir), "metrics.json")

    params = TrainingPipelineParams(
        input_data_path=fake_dataset_path,
        output_model_path=expected_output_model_path,
        metric_path=expected_metric_path,
        splitting_params=SplittingParams(),
        model_params=ModelParams()
    )

    real_model_path, metrics = train_pipeline(params)
    assert metrics["mae"] >= 0
    assert os.path.exists(real_model_path)
    assert os.path.exists(params.metric_path)
