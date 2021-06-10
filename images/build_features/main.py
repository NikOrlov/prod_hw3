import numpy as np
import click
import re
import os
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
import pickle


def numerical_pipeline(df: pd.DataFrame) -> Pipeline:
    pipe = Pipeline([('imputer', SimpleImputer(missing_values=np.nan, strategy='mean')),
                     ('normalizer', StandardScaler())])
    pipe.fit(df)
    return pipe


def make_features(df: pd.DataFrame, pipeline: Pipeline) -> pd.DataFrame:
    df_featured = pipeline.transform(df)
    return pd.DataFrame(df_featured)


@click.command()
@click.argument("path_raw")
def build_features(path_raw: str):

    csv_args = {'sep': ',', 'header': None}
    path_processed = re.subn('/raw/', '/processed/', path_raw)[0]
    os.makedirs(path_processed, exist_ok=True)

    df_raw = pd.read_csv(f'{path_raw}/data.csv', **csv_args)
    df_raw_target = pd.read_csv(f'{path_raw}/target.csv', **csv_args)

    # create and save pipeline for further transformations
    features_pipeline = numerical_pipeline(df_raw)
    path_transformer = re.subn('/raw/', '/model/', path_raw)[0]

    os.makedirs(path_transformer, exist_ok=True)
    with open(f'{path_transformer}/transformer.pkl', 'wb') as file:
        pickle.dump(features_pipeline, file)

    csv_args = {'sep': ',', 'header': False, 'index': False}
    df_featured = make_features(df_raw, features_pipeline)

    df_featured.to_csv(f'{path_processed}/train_val.csv', **csv_args)
    assert df_raw.shape == df_featured.shape

    # Dummy transformation for target
    df_featured_target = df_raw_target
    df_featured_target.to_csv(f"{path_processed}/target.csv", **csv_args)
    assert df_raw_target.shape == df_featured_target.shape
    assert len(df_featured) == len(df_featured_target)


if __name__ == "__main__":
    build_features()
