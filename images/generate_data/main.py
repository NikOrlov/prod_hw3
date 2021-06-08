import numpy as np
from sklearn import datasets
import click
import os
import pandas as pd


@click.command()
@click.argument('output_dir')
def get_data(output_dir: str):

    data, target = datasets.load_breast_cancer(return_X_y=True)

    subset_size = np.random.randint(5, len(data))
    subset_idx = np.random.choice(len(data), subset_size)

    train = data[subset_idx]
    target = target[subset_idx]

    assert len(train) == len(target)

    os.makedirs(output_dir, exist_ok=True)
    csv_args = {'sep': ',', 'header': False, 'index': False}

    pd.DataFrame(train).to_csv(f'{output_dir}/data.csv', **csv_args)
    pd.DataFrame(target).to_csv(f'{output_dir}/target.csv', **csv_args)


if __name__ == '__main__':
    get_data()
