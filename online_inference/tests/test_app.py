import pytest
from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)

CORRECT_DATA = [1, 1, 1, 1, 1, 1]
INCORRECT_DATA = [1, 1, 1, 1, 1, 'a']
SHORT_DATA = [1, 1, 1]


@pytest.mark.parametrize(
    'data_sample, response',
    [
        (CORRECT_DATA, 200),
        (INCORRECT_DATA, 400),
        (SHORT_DATA, 400),
    ]
)
def test_predict(data_sample, response):
    response = client.get("/predict/", json={'data': [data_sample]})
    return response.status_code
