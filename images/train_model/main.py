from sklearn.ensemble import RandomForestClassifier
import click
import pandas as pd
import re
import pickle
import os


@click.command()
@click.argument('path')
def train_model(path: str):

    csv_args = {'sep': ',', 'header': None}
    x_train = pd.read_csv(f'{path}/x_train.csv', **csv_args)
    y_train = pd.read_csv(f'{path}/y_train.csv', **csv_args)
    model = RandomForestClassifier()
    model.fit(x_train, y_train)

    model_path = re.subn('/processed/', '/model/', path)[0]
    os.makedirs(model_path, exist_ok=True)

    with open(f'{model_path}/model.pkl', 'wb') as file:
        pickle.dump(model, file)


if __name__ == "__main__":
    train_model()
