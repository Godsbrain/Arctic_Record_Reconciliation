from rapidfuzz import fuzz
import pandas as pd


def compute_similarity(row1, row2):
    """
    Compute similarity score between two records
    """
    name1 = f"{row1['first_name']} {row1['last_name']}"
    name2 = f"{row2['first_name']} {row2['last_name']}"

    name_score = fuzz.ratio(name1, name2) / 100

    # Birth year similarity
    if pd.isna(row1['birth_year']) or pd.isna(row2['birth_year']):
        birth_score = 0
    else:
        birth_score = 1 if row1['birth_year'] == row2['birth_year'] else 0

    # Community similarity
    community_score = fuzz.ratio(
        str(row1['community']),
        str(row2['community'])
    ) / 100

    # Final weighted score
    total_score = (
        0.6 * name_score +
        0.3 * birth_score +
        0.1 * community_score
    )

    return total_score


def find_matches(df):
    """
    Compare all records and find matches
    """
    matches = []

    for i in range(len(df)):
        for j in range(i + 1, len(df)):

            score = compute_similarity(df.iloc[i], df.iloc[j])

            if score > 0.8:
                matches.append({
                    "record_1": i,
                    "record_2": j,
                    "score": score
                })

    return pd.DataFrame(matches)