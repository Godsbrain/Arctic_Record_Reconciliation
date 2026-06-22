import pandas as pd


def identify_priority_cases(matches_df, quality_df):

    # ======================
    # 🔹 Detect column format (VERY IMPORTANT)
    # ======================
    if "record1_id" in matches_df.columns:
        col1 = "record1_id"
        col2 = "record2_id"
    else:
        col1 = "record1"
        col2 = "record2"

    # ======================
    # 🔹 Merge for record1
    # ======================
    merged_1 = matches_df.merge(
        quality_df,
        left_on=col1,
        right_on="record_id",
        how="left"
    ).rename(columns={
        "manual_review": "manual_review_1",
        "completeness_score": "completeness_1"
    })

    # ======================
    # 🔹 Merge for record2
    # ======================
    merged_full = merged_1.merge(
        quality_df,
        left_on=col2,
        right_on="record_id",
        how="left"
    ).rename(columns={
        "manual_review": "manual_review_2",
        "completeness_score": "completeness_2"
    })

    # ======================
    # 🔹 Priority logic
    # ======================
    priority_cases = merged_full[
        (merged_full["category"].isin(["High Match", "Possible Match"])) &
        (
            merged_full["manual_review_1"] |
            merged_full["manual_review_2"]
        )
    ]

    return priority_cases