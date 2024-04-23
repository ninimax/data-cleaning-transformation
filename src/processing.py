import os

import pandas as pd

from src import quality_checks, logger

app_logger = logger.create_logger(logger.LoggerType.APPLICATION)
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def drop_duplicates(df):
    return df.drop_duplicates(keep="first", inplace=False)


def merge(df1, df2, column_name):
    return pd.merge(df1, df2, on=column_name, how="inner")


def standardize_text_lower_stripped(df, column_name):
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
    """#
    I was about to implement it but then I found out that, it seems to be more
    complex than it looks like with first glance, since the data quality is
    not ensured to begin with...
    e.g.
    TRK001,15-06-2023,122181
    TRK001,06-07-2023,195456
    TRK001,23-09-2023,49353
    TRK001,28-10-2023,80467

    The mileage of truck with id TRK001
    is reduced from 195456(06-07-2023) to 49353 (23-09-2023).
    That is logically wrong and would need to confirm with the source provider
    TODO
    """
    pass


def export_to_csv(df, path):
    df.to_csv(path, index=False)


def delete_file(path):
    if os.path.exists(path) and os.path.isfile(path):
        os.remove(path)
        app_logger.info(
            f"already existing a file, file deleted, path: {path}")
    else:
        app_logger.error(f"file not found, path: {path}")
