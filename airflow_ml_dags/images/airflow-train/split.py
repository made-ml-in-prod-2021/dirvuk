import os

import click
import pandas as pd
from sklearn.model_selection import train_test_split


@click.command()
@click.option("--input_dir")
def split(input_dir):
    TRAIN_SIZE = 0.7

    X = pd.read_csv(os.path.join(input_dir, "data.csv"))
    y = pd.read_csv(os.path.join(input_dir, "target.csv"))

    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=TRAIN_SIZE)

    X_train.to_csv(os.path.join(input_dir, "x_train.csv"), index=None)
    X_test.to_csv(os.path.join(input_dir, "x_test.csv"), index=None)
    y_train.to_csv(os.path.join(input_dir, "y_train.csv"), index=None)
    y_test.to_csv(os.path.join(input_dir, "y_test.csv"), index=None)


if __name__ == '__main__':
    split()
