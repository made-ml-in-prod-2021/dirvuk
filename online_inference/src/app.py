import os
import uvicorn
import pickle

from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

PATH_TO_MODEL = 'model/model.pkl'


def load_object(path: str) -> object:
    with open(path, "rb") as f:
        return pickle.load(f)


class PredictionModel(BaseModel):
    data: List


class Response(BaseModel):
    prediction: int


model: Optional[object] = None
partial_models: List[object] = []


def make_predict(
        data: List, model: object,
) -> List[Response]:
    predicts = model.predict(data)
    return predicts


app = FastAPI()


@app.get("/")
def main():
    return "it is entry point"


@app.on_event("startup")
def load_models():
    global model
    model = load_object(PATH_TO_MODEL)


@app.get("/health")
def health() -> bool:
    return not (model is None)


@app.get("/predict/", response_model=int)
def predict(request: PredictionModel):
    print(request.data)
    if len(request.data[0]) != 14:
        raise HTTPException(status_code=400, detail="Expected sample length shall be 14")

    if len([(isinstance(data_item, int) or isinstance(data_item, int)) for data_item in request.data[0]]) != 14:
        raise HTTPException(status_code=400, detail="Expect only floats or ints in input data")

    return make_predict(request.data, model)


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=os.getenv("PORT", 8000))
