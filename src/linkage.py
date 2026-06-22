from rapidfuzz import fuzz
import pandas as pd


def find_matches(df1, df2=None):
    """
    Supports:
    - Single dataset (df1 only) → internal matching
    - Dual dataset (df1 vs df2) → reconciliation matching
    """

    results = []

    # ======================
    # 🔹 CASE 1: SINGLE DATASET
    # ======================
    if df2 is None:
        for i, row1 in df1.iterrows():
            for j, row2 in df1.iterrows():
                if i >= j:
                    continue  # Avoid duplicate/self comparison

                name_score = fuzz.token_sort_ratio(
                    str(row1.get("first_name", "")) + " " + str(row1.get("last_name", "")),
                    str(row2.get("first_name", "")) + " " + str(row2.get("last_name", ""))
                )

                birth_diff = abs(
                    (row1.get("birth_year", 0) or 0) -
                    (row2.get("birth_year", 0) or 0)
                )

                # combined score
                score = name_score - (birth_diff * 2)

                if score > 85:
                    category = "High Match"
                elif score > 70:
                    category = "Possible Match"
                else:
                    continue

                results.append({
                    "record1": i,
                    "record2": j,
                    "name1": f"{row1.get('first_name')} {row1.get('last_name')}",
                    "name2": f"{row2.get('first_name')} {row2.get('last_name')}",
                    "score": score,
                    "category": category
                })

    # ======================
    # 🔹 CASE 2: DUAL DATASET (MAIN USE CASE)
    # ======================
    else:
        for i, row1 in df1.iterrows():
            for j, row2 in df2.iterrows():

                # ---- NAME SIMILARITY ----
                name1 = f"{row1.get('first_name', '')} {row1.get('last_name', '')}"
                name2 = f"{row2.get('first_name', '')} {row2.get('last_name', '')}"

                name_score = fuzz.token_sort_ratio(name1, name2)

                # ---- BIRTH YEAR DIFFERENCE ----
                birth1 = row1.get("birth_year", 0) or 0
                birth2 = row2.get("birth_year", 0) or 0

                birth_diff = abs(birth1 - birth2)

                # ---- LOCATION SIMILARITY (optional boost) ----
                loc1 = str(row1.get("community", ""))
                loc2 = str(row2.get("community", ""))

                location_score = fuzz.partial_ratio(loc1, loc2)

                # ---- FINAL SCORE ----
                score = (
                    name_score * 0.6 +
                    location_score * 0.2 +
                    max(0, 100 - birth_diff * 10) * 0.2
                )

                # ---- CLASSIFICATION ----
                if score >= 85:
                    category = "High Match"
                elif score >= 70:
                    category = "Possible Match"
                elif score >= 55:
                    category = "Manual Review"
                else:
                    continue

                results.append({
                    "record1_id": row1.get("id", i),
                    "record2_id": row2.get("id", j),
                    "name1": name1,
                    "name2": name2,
                    "birth1": birth1,
                    "birth2": birth2,
                    "location1": loc1,
                    "location2": loc2,
                    "score": round(score, 2),
                    "category": category
                })

    return pd.DataFrame(results)