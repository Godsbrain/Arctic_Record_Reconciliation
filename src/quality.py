import pandas as pd


def calculate_completeness(row):
    """
    Calculate how complete a record is (percentage)
    """
    fields = ["first_name", "last_name", "birth_year", "community"]

    filled = sum([1 for f in fields if pd.notna(row[f])])
    total = len(fields)

    return round((filled / total) * 100, 2)


def count_missing(row):
    """
    Count missing fields
    """
    fields = ["first_name", "last_name", "birth_year", "community"]

    return sum([1 for f in fields if pd.isna(row[f])])


def assess_quality(df):
    """
    Assess data quality for entire dataset
    """
    results = []

    for i in range(len(df)):
        row = df.iloc[i]

        completeness = calculate_completeness(row)
        missing = count_missing(row)

        results.append({
            "record_id": i,
            "completeness_score": completeness,
            "missing_fields": missing,
            "manual_review": True if completeness <= 75 else False

        })

    return pd.DataFrame(results)