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

    return {
        "total": total_score,
        "name": name_score,
        "birth": birth_score,
        "community": community_score
    }


def categorize_score(score):
    """
    Assign category based on score
    """
    if score >= 0.9:
        return "High Match"
    elif score >= 0.7:
        return "Possible Match"
    elif score >= 0.5:
        return "Manual Review"
    else:
        return "Low Match"


def find_matches(df):
    """
    Compare all records and find matches
    """
    matches = []

    for i in range(len(df)):
        for j in range(i + 1, len(df)):

            scores = compute_similarity(df.iloc[i], df.iloc[j])
            total_score = scores["total"]

            if total_score > 0.5:
                matches.append({
                    "record_1": i,
                    "record_2": j,
                    "score": total_score,
                    "category": categorize_score(total_score),
                    "name_score": scores["name"],
                    "birth_score": scores["birth"],
                    "community_score": scores["community"]
                })

    return pd.DataFrame(matches)


if __name__ == "__main__":
    from src.cleaning import clean_dataset
    from src.database import get_engine

    df = clean_dataset("data/raw/sample_records.csv")

    matches = find_matches(df)

    engine = get_engine()

    matches.to_sql("record_matches", con=engine, if_exists="replace", index=False)

    print("✅ Matches saved to database!")
    print(matches)