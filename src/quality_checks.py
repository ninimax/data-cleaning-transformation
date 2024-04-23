import re


def count_full_duplicates(df):
    return df.duplicated(keep=False).sum()


def count_missing_val_per_col(df):
    return df.isna().sum()


def get_items_existing_in_df1_only(df1, df2, column_name):
    mask = ~df1[column_name].isin(df2[column_name])
    ids_only_in_df1_but_not_df2 = df1.loc[mask, column_name].unique()
    return ids_only_in_df1_but_not_df2


def validate_email(email):
    regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(regex, email))
