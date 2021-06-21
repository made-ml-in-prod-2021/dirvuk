import os

import click
import pandas as pd


@click.command()
@click.option("--input_dir")
@click.option("--output_dir")
def preprocess(input_dir, output_dir):
    X = pd.read_csv(os.path.join(input_dir, "data.csv"))
    y = pd.read_csv(os.path.join(input_dir, "target.csv"))

    os.makedirs(output_dir, exist_ok=True)
    X.to_csv(os.path.join(output_dir, "data.csv"), index=False)
    y.to_csv(os.path.join(output_dir, "target.csv"), index=False)


if __name__ == '__main__':
    preprocess()
