import json
import click
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, precision_score, recall_score
import pickle
import pandas as pd
import re


@click.command()
@click.argument('path')
def validate(path: str):
    with open(f'{path}/model.pkl', 'rb') as file:
        model = pickle.load(file)

    csv_args = {'sep': ',', 'header': None}
    data_path = re.subn('/model/', '/processed/', path)[0]
    df_x_val = pd.read_csv(f'{data_path}/x_val.csv', **csv_args)
    df_y_val = pd.read_csv(f'{data_path}/y_val.csv', **csv_args)

    preds = model.predict(df_x_val)
    metrics = dict()
    metrics['accuracy'] = round(accuracy_score(df_y_val, preds), 4)
    metrics['roc_auc'] = round(roc_auc_score(df_y_val, preds), 4)
    metrics['f1'] = round(f1_score(df_y_val, preds), 4)
    metrics['precision'] = round(precision_score(df_y_val, preds), 4)
    metrics['recall'] = round(recall_score(df_y_val, preds), 4)

    with open(f'{path}/metrics.json', 'w') as file:
        json.dump(metrics, file)


if __name__ == "__main__":
    validate()
