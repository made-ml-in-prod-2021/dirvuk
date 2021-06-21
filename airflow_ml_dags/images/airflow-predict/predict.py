import os
import pickle

import click
import pandas as pd


@click.command()
@click.option("--input_dir")
@click.option("--output_dir")
@click.option("--model_path")
def predict(input_dir, output_dir, model_path):
    X = pd.read_csv(os.path.join(input_dir, "data.csv"))
    predict_path = os.path.join(output_dir, "predictions.csv")

    with open(model_path, "rb") as f:
        clf = pickle.load(f)
        y_pred = clf.predict(X)
        data = pd.DataFrame(y_pred, columns=["target"])
        os.makedirs(output_dir, exist_ok=True)
        data.to_csv(predict_path, index=False)


if __name__ == '__main__':
    predict()
