import pickle
import click
import pandas as pd
import re
import os


@click.command('predict')
@click.argument('data_path')
@click.argument('model_path')
def predict(data_path: str, model_path: str):

    print(data_path, model_path)
    model_path = re.subn('/raw/', '/model/', data_path)[0]
    with open(f'{model_path}/model.pkl', 'rb') as file:
        model = pickle.load(file)

    df_data = pd.read_csv(f'{data_path}/data.csv', sep=',', header=None)

    predictions = model.predict(df_data)
    predictions_path = re.subn('/raw/', '/predictions/', data_path)[0]
    os.makedirs(predictions_path, exist_ok=True)
    pd.DataFrame(predictions).to_csv(f'{predictions_path}/predictions.csv', sep=',', index=False, header=False)


if __name__ == '__main__':
    predict()
