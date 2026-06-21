import pandas as pd


def identify_priority_cases(matches_df, quality_df):

    # Merge for record_1
    merged_1 = matches_df.merge(
        quality_df,
        left_on="record_1",
        right_on="record_id",
        how="left"
    ).rename(columns={
        "manual_review": "manual_review_1",
        "completeness_score": "completeness_1"
    })

    # Merge for record_2
    merged_full = merged_1.merge(
        quality_df,
        left_on="record_2",
        right_on="record_id",
        how="left"
    ).rename(columns={
        "manual_review": "manual_review_2",
        "completeness_score": "completeness_2"
    })

    # Priority rule
    priority_cases = merged_full[
        (merged_full["category"].isin(["High Match", "Possible Match"])) &
        (
            (merged_full["manual_review_1"] == True) |
            (merged_full["manual_review_2"] == True)
        )
    ]

    return priority_cases