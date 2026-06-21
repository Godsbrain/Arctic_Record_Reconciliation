import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from src.cleaning import clean_dataset
from src.linkage import find_matches
from src.quality import assess_quality
from src.investigation import identify_priority_cases


# ======================
# 🧱 HEADER
# ======================

st.title("Arctic Record Reconciliation System")

st.write(
    "Analyze historical records using matching, data quality scoring, "
    "and investigation prioritization."
)

# ======================
# 📂 LOAD DATA
# ======================

df = clean_dataset("data/raw/sample_records.csv")

matches = find_matches(df)
quality = assess_quality(df)
priority = identify_priority_cases(matches, quality)

# ======================
# 📌 KEY METRICS (NEW)
# ======================

st.subheader("📌 Key Metrics")

m1, m2, m3 = st.columns(3)

m1.metric("Total Records", len(df))
m2.metric("Matches Found", len(matches))
m3.metric("Priority Cases", len(priority))

# ======================
# 📊 DASHBOARD CHARTS
# ======================

st.subheader("📊 Overview")

col1, col2 = st.columns(2)

col1.subheader("Match Distribution")
col1.bar_chart(matches["category"].value_counts())

col2.subheader("Data Quality (Review Needed)")
col2.bar_chart(quality["manual_review"].value_counts())

# ======================
# 🔍 SEARCH SECTION
# ======================

st.subheader("🔍 Search Records")

search_name = st.text_input("Enter First Name")

if search_name:
    results = df[df["first_name"].str.contains(search_name, case=False)]
    st.dataframe(results)

# ======================
# 📊 MATCH RESULTS
# ======================

# ======================
# 📊 MATCH RESULTS
# ======================

st.subheader("📊 Match Results")

# Create a copy of matches
styled_matches = matches.copy()

# Add emoji-based coloring
def category_color(val):
    if val == "High Match":
        return "🟢 " + val
    elif val == "Possible Match":
        return "🟡 " + val
    elif val == "Manual Review":
        return "🔴 " + val
    return val

# Apply transformation
styled_matches["category"] = styled_matches["category"].apply(category_color)

# Display table
st.dataframe(styled_matches)
# ======================
# 🧪 DATA QUALITY
# ======================

st.subheader("🧪 Data Quality Assessment")
st.dataframe(quality)

# ======================
# 🚨 PRIORITY CASES
# ======================

st.subheader("🚨 Priority Investigation Cases")

if not priority.empty:
    st.error("⚠️ High Priority Cases Detected")
    st.dataframe(priority)
else:
    st.success("✅ No priority cases found")
