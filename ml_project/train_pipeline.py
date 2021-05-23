import json
import logging
import sys

import click

from data.make_dataset import read_data, split_train_val_data
from models.models_fit_predict import (
    serialize_model,
    train_model,
    evaluate_model,
    predict_model,
)

from train_pipeline_params import (
    TrainingPipelineParams,
    read_training_pipeline_params,
)

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


def train_pipeline(training_pipeline_params: TrainingPipelineParams):
    data = read_data(training_pipeline_params.input_data_path)
    logger.info(f"data.shape is {data.shape}")
    train_df, val_df = split_train_val_data(data, training_pipeline_params.splitting_params)

    logger.info(f"train_df.shape is {train_df.shape}")
    logger.info(f"val_df.shape is {val_df.shape}")

    train_features = train_df.drop(['target'], axis=1)
    train_target = train_df['target']

    val_features = val_df.drop(['target'], axis=1)
    val_target = val_df['target']

    model = train_model(train_features, train_target, training_pipeline_params.model_params)

    predicts = predict_model(
        model,
        val_features
    )

    metrics = evaluate_model(
        predicts,
        val_target
    )

    with open(training_pipeline_params.metric_path, "w") as metric_file:
        json.dump(metrics, metric_file)
    logger.info(f"metrics is {metrics}")

    path_to_model = serialize_model(model, training_pipeline_params.output_model_path)
    return path_to_model, metrics


@click.command(name="train_pipeline")
@click.argument("config_path")
def train_pipeline_command(config_path: str):
    params = read_training_pipeline_params(config_path)
    train_pipeline(params)


if __name__ == "__main__":
    train_pipeline_command()
