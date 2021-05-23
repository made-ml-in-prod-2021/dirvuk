import os

import pytest

from enities.split_params import SplittingParams
from data.make_dataset import read_data, split_train_val_data


@pytest.fixture()
def dataset_path():
    curdir = os.path.dirname(__file__)
    return os.path.join(curdir, "train_data_sample.csv")


@pytest.fixture()
def target_col():
    return "target"


def test_load_dataset(dataset_path: str, target_col: str):
    data = read_data(dataset_path)
    assert len(data) > 5
    assert target_col in data.keys()


def test_split_dataset(dataset_path: str):
    val_size = 0.2
    splitting_params = SplittingParams(random_state=239, val_size=val_size, )
    data = read_data(dataset_path)
    train, val = split_train_val_data(data, splitting_params)
    assert train.shape[0] > 5
    assert val.shape[0] > 1
