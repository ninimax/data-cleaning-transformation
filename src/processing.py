import pandas as pd


def merge(df1, df2, column_name):
    return pd.merge(df1, df2, on=column_name, how="inner")


def standardize_text(df, column_name):
    df[column_name] = df[column_name].str.lower().str.strip()
    return df


def standardize_dates(df, column_name):
    df[column_name] = pd.to_datetime(df[column_name], format='%d-%m-%Y', errors='coerce')
    return df


def encode_one_hot(df, column_name):
    one_hot_encoded = pd.get_dummies(df[column_name])
    df_encoded = pd.concat([df, one_hot_encoded], axis=1)
    return df_encoded


def add_column(series):
    return None


def validate(df):
    return None
