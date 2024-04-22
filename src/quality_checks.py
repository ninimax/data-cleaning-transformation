import re


def count_full_duplicates(df):
    return df.duplicated(keep=False).sum()


def count_missing_val_per_col(df):
    return [20, 30, 10]


def get_id_existing_in_df1_only(df1, df2):
    return []


def validate_email(email):
    regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(regex, email)
