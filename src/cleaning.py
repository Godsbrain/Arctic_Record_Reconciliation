import pandas as pd


def standardize_names(df, column):
    """
    Convert names to Title Case
    """
    df[column] = df[column].str.strip().str.title()
    return df


def remove_duplicates(df):
    """
    Remove duplicate rows
    """
    return df.drop_duplicates()


def handle_missing_values(df):
    """
    Fill missing values
    """
    df = df.fillna({
        "first_name": "Unknown",
        "last_name": "Unknown",
        "community": "Unknown"
    })
    return df


def clean_dataset(file_path):
    """
    Full cleaning pipeline
    """
    df = pd.read_csv(file_path)

    df = standardize_names(df, "first_name")
    df = standardize_names(df, "last_name")

    df = remove_duplicates(df)
    df = handle_missing_values(df)

    return df