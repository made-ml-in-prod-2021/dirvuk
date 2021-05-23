import pickle
import pandas as pd
import numpy as np

from typing import Dict

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

from enities.model_params import ModelParams


def train_model(features: pd.DataFrame, target: pd.Series, model_params: ModelParams):
    if model_params.model_type == 'RandomForestClassifier':
        model = RandomForestClassifier(
            max_depth=model_params.max_depth,
            min_samples_leaf=model_params.min_samples_leaf,
            min_samples_split=model_params.min_samples_split,
            n_estimators=model_params.n_estimators,
            n_jobs=model_params.n_jobs
        )
    elif model_params.model_type == 'LinearRegression':
            model = LinearRegression(
                n_jobs=model_params.n_jobs
            )
    else:
        raise NotImplementedError()

    model.fit(features, target)
    return model


def make_features(transformer: ColumnTransformer, df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(transformer.transform(df).toarray())


def serialize_model(model: RandomForestClassifier, output: str) -> str:
    with open(output, "wb") as f:
        pickle.dump(model, f)

    return output


def evaluate_model(
        predicts: np.ndarray, target: pd.Series
) -> Dict[str, float]:
    return {
        "mae": mean_absolute_error(target, predicts),
    }


def predict_model(
        model: RandomForestClassifier, features: pd.DataFrame
) -> np.ndarray:
    predicts = model.predict(features)
    return predicts
