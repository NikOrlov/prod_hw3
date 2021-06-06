from sklearn.model_selection import train_test_split
import pandas as pd
import click


@click.command()
@click.argument("path")
def split_data(path: str):

    csv_args = {'sep': ',', 'header': None}
    df_data = pd.read_csv(f"{path}/train_val.csv", **csv_args)
    df_target = pd.read_csv(f"{path}/target.csv", **csv_args)

    random_seed = 42
    x_train, x_val, y_train, y_val = train_test_split(df_data, df_target, test_size=0.3, random_state=random_seed)

    assert len(x_val) == len(y_val)
    assert len(x_train) == len(y_train)
    assert x_train.shape[1] == x_val.shape[1]

    csv_args = {'sep': ',', 'header': False, 'index': False}
    x_train.to_csv(f"{path}/x_train.csv", **csv_args)
    x_val.to_csv(f"{path}/x_val.csv", **csv_args)
    y_train.to_csv(f"{path}/y_train.csv", **csv_args)
    y_val.to_csv(f"{path}/y_val.csv", **csv_args)


if __name__ == "__main__":
    split_data()
