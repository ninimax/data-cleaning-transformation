import os

import pandas as pd

pd.options.mode.chained_assignment = None  # default='warn'

from src import quality_checks

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def drop_duplicates(df):
    return df.drop_duplicates(keep="first", inplace=False)


def merge(df1, df2, column_name):
    return pd.merge(df1, df2, on=column_name, how="inner")


def standardize_text(df, column_name):
    df[column_name] = df[column_name].str.lower().str.strip()
    return df


def standardize_dates(df, column_name):
    df[column_name] = pd.to_datetime(df[column_name],
                                     format='%d-%m-%Y',
                                     errors='coerce',
                                     dayfirst=True)
    return df


def encode_one_hot(df, column_name):
    one_hot_encoded = pd.get_dummies(df[column_name], prefix=column_name)
    df_encoded = pd.concat([df, one_hot_encoded], axis=1)
    df_encoded.drop(column_name, axis=1, inplace=True)
    return df_encoded


def add_column_email_valid(df, column_name):
    df["email_valid"] = df[column_name].apply(quality_checks.validate_email)
    return df


def calc_cost_per_km(df, column_name):
    # TODO
    pass


def export_to_csv(df, path):
    df.to_csv(path, index=False)
