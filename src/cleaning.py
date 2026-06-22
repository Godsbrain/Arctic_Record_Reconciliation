import pandas as pd


def standardize_names(df, column):
    """
    Convert names to Title Case safely
    """
    if column in df.columns:
        df[column] = df[column].astype(str).str.strip().str.title()
    return df


def remove_duplicates(df):
    """
    Remove duplicate rows
    """
    return df.drop_duplicates()


def create_community_column(df):
    """
    Create a 'community' column if missing
    """
    if "community" not in df.columns:

        if "province" in df.columns and "district" in df.columns:
            df["community"] = (
                df["province"].fillna("").astype(str) + ", " +
                df["district"].fillna("").astype(str)
            )

        elif "subdistrict" in df.columns:
            df["community"] = df["subdistrict"].fillna("Unknown").astype(str)

        else:
            df["community"] = "Unknown"

    return df


def handle_missing_values(df):
    """
    Fill missing values safely
    """
    if "first_name" in df.columns:
        df["first_name"] = df["first_name"].fillna("Unknown")

    if "last_name" in df.columns:
        df["last_name"] = df["last_name"].fillna("Unknown")

    if "community" in df.columns:
        df["community"] = df["community"].fillna("Unknown")

    if "birth_year" in df.columns:
        df["birth_year"] = df["birth_year"].fillna(0)

    return df


def ensure_id_column(df):
    """
    Ensure every record has an ID
    """
    if "id" not in df.columns:
        df["id"] = df.index
    return df


def clean_dataset(file_path):
    """
    Full cleaning pipeline
    """
    df = pd.read_csv(file_path)

    # ✅ Create required columns FIRST
    df = create_community_column(df)

    # ✅ Standardize names
    df = standardize_names(df, "first_name")
    df = standardize_names(df, "last_name")

    # ✅ Remove duplicates
    df = remove_duplicates(df)

    # ✅ Handle missing values
    df = handle_missing_values(df)

    # ✅ Ensure ID exists
    df = ensure_id_column(df)

    return df