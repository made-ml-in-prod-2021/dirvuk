import os
import pickle

import click
import pandas as pd
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC


@click.command()
@click.option("--input_dir")
@click.option("--model_dir")
def train(input_dir, model_dir):

    X_train = pd.read_csv(os.path.join(input_dir, "x_train.csv"))
    y_train = pd.read_csv(os.path.join(input_dir, "y_train.csv"))

    clf = OneVsRestClassifier(LinearSVC())
    clf.fit(X_train, y_train)

    os.makedirs(model_dir, exist_ok=True)

    model_dir = os.path.join(model_dir, "model.pkl")

    with open(model_dir, "wb") as f:
        pickle.dump(clf, f)


if __name__ == '__main__':
    train()
