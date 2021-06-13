import os
import pickle

import click
import pandas as pd
from sklearn.metrics import classification_report


@click.command()
@click.option("--input_dir")
@click.option("--model_dir")
def validate(input_dir, model_dir):

    X = pd.read_csv(os.path.join(input_dir, "x_test.csv"))
    y = pd.read_csv(os.path.join(input_dir, "y_test.csv"))

    model_path = os.path.join(model_dir, "model.pkl")
    report_path = os.path.join(model_dir, "report.txt")

    with open(model_path, "rb") as f:
        model = pickle.load(f)
    y_pred = model.predict(X)
    report = classification_report(y, y_pred)

    with open(report_path, "w") as f:
        f.writelines(report)


if __name__ == '__main__':
    validate()
