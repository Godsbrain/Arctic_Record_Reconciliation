import sys
import os
import pandas as pd
import streamlit as st

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.cleaning import clean_dataset
from src.linkage import find_matches
from src.quality import assess_quality
from src.investigation import identify_priority_cases


# ======================
# 🧱 HEADER
# ======================

st.title("Arctic Record Reconciliation System")

st.markdown("""
Analyze historical records using **record matching**, **data quality scoring**,  
and **investigation prioritization**.
""")

with st.expander("ℹ️ About This Project"):
    st.write("""
    This system demonstrates how data reconciliation techniques can be applied 
    to historical datasets to identify inconsistencies, match records, 
    and prioritize cases requiring investigation.
    """)

# ======================
# 📂 DATA SELECTION
# ======================

data_option = st.selectbox(
    "Select Dataset",
    ["Sample Data", "Real Census Data"]
)

# ======================
# 📂 LOAD DATA
# ======================

if data_option == "Sample Data":
    df = clean_dataset("data/raw/sample_records.csv")

    # ✅ Ensure ID exists
    if "id" not in df.columns:
        df["id"] = df.index

    matches = find_matches(df)
    quality = assess_quality(df)
    priority = identify_priority_cases(matches, quality)

else:
    df1 = clean_dataset("data/processed/cleaned_census_final_data.csv")
    df2 = clean_dataset("data/processed/parish_data.csv")

    # ✅ PERFORMANCE FIX
    df1 = df1.head(500)
    df2 = df2.head(500)

    # ✅ Ensure ID exists in BOTH
    if "id" not in df1.columns:
        df1["id"] = df1.index
    if "id" not in df2.columns:
        df2["id"] = df2.index

    matches = find_matches(df1, df2)

    df1["source"] = "Census"
    df2["source"] = "Parish"

    df = pd.concat([df1, df2], ignore_index=True)

    quality = assess_quality(df)
    priority = identify_priority_cases(matches, quality)

# ======================
# 📌 METRICS
# ======================

st.subheader("📌 Key Metrics")

total_records = len(df)
total_matches = len(matches)
high_matches = len(matches[matches["category"] == "High Match"])

m1, m2, m3, m4 = st.columns(4)

m1.metric("Total Records", total_records)
m2.metric("Matches", total_matches)
m3.metric("High Matches", high_matches)
m4.metric("Match Rate", f"{(total_matches / total_records * 100):.1f}%" if total_records else "0%")

# ======================
# 🎯 FILTER
# ======================

st.subheader("🎯 Filter Matches")

filter_option = st.selectbox(
    "Select Category",
    ["All", "High Match", "Possible Match", "Manual Review"]
)

filtered_matches = matches if filter_option == "All" else matches[matches["category"] == filter_option]

# ======================
# 📊 DASHBOARD
# ======================

st.subheader("📊 Dashboard")

col1, col2 = st.columns(2)

with col1:
    if not matches.empty:
        st.bar_chart(matches["category"].value_counts())

with col2:
    if not matches.empty:
        st.bar_chart(matches["score"].round().value_counts().sort_index())

# ======================
# 🌍 MAP
# ======================

st.subheader("🌍 Map View")

if "community" in df.columns:
    map_df = df.copy()

    map_df["lat"] = 49.0 + (map_df.index % 10) * 0.1
    map_df["lon"] = -97.0 + (map_df.index % 10) * 0.1

    st.map(map_df[["lat", "lon"]])

# ======================
# 🔍 SEARCH
# ======================

st.subheader("🔍 Search")

search = st.text_input("Search First Name")

if search:
    results = df[df["first_name"].str.contains(search, case=False, na=False)]
    st.dataframe(results, width="stretch")

# ======================
# 📊 MATCH RESULTS
# ======================

st.subheader("📊 Match Results")

if not filtered_matches.empty:
    table = filtered_matches.copy()

    table["category"] = table["category"].map({
        "High Match": "🟢 High",
        "Possible Match": "🟡 Medium",
        "Manual Review": "🔴 Review"
    })

    st.dataframe(table, width="stretch")

    csv = filtered_matches.to_csv(index=False)
    st.download_button("📥 Download Matches", csv, "matches.csv")

else:
    st.warning("No matches found")

# ======================
# 🔍 COMPARISON VIEW
# ======================

st.subheader("🔍 Record Comparison")

if not filtered_matches.empty:

    selected_index = st.selectbox("Select Match", filtered_matches.index)
    row = filtered_matches.loc[selected_index]

    if "record1_id" in row:
        id1, id2 = row["record1_id"], row["record2_id"]
    else:
        id1, id2 = row["record1"], row["record2"]

    rec1 = df[df["id"] == id1]
    rec2 = df[df["id"] == id2]

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Record 1")
        st.dataframe(rec1, width="stretch")

    with col2:
        st.write("### Record 2")
        st.dataframe(rec2, width="stretch")

    # ✅ Differences
    st.write("### Differences")

    if not rec1.empty and not rec2.empty:
        r1, r2 = rec1.iloc[0], rec2.iloc[0]

        diff = {}
        for col in ["first_name", "last_name", "birth_year", "community"]:
            if col in r1 and col in r2 and r1[col] != r2[col]:
                diff[col] = (r1[col], r2[col])

        if diff:
            st.dataframe(pd.DataFrame(diff, index=["Record 1", "Record 2"]).T)
        else:
            st.success("No major differences")

# ======================
# 🧪 QUALITY
# ======================

st.subheader("🧪 Data Quality")

if not quality.empty:
    st.dataframe(quality, width="stretch")

# ======================
# 🚨 PRIORITY
# ======================

st.subheader("🚨 Priority Cases")

if not priority.empty:
    st.error(f"{len(priority)} Priority Cases")
    st.dataframe(priority, width="stretch")
else:
    st.success("No priority cases")