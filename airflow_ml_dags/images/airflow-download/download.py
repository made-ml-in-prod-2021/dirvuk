import os

import click
from sklearn.datasets import load_iris


@click.command()
@click.option("--output_dir")
def download(output_dir: str):
    X, y = load_iris(return_X_y=True, as_frame=True)

    os.makedirs(output_dir, exist_ok=True)

    X.to_csv(os.path.join(output_dir, "data.csv"), index=None)
    y.to_csv(os.path.join(output_dir, "target.csv"), index=None)


if __name__ == '__main__':
    download()
