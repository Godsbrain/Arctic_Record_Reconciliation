\# Arctic Record Reconciliation System



\## 🚀 Live App

https://arctic-record-reconciliation.streamlit.app/



\---



\## 📌 Overview



This project is an end-to-end \*\*data reconciliation and investigation system\*\* designed to identify duplicate or related records across multiple datasets.



It simulates real-world workflows by linking \*\*census and parish records\*\*, evaluating \*\*data quality\*\*, and prioritizing cases that require human review.



The system integrates data processing, record linkage, and analytics into an interactive dashboard for analysts and decision-makers.



\---



\## 📸 Dashboard Preview


## 📸 Dashboard Preview

### 📊 Dashboard
![Dashboard](images/dashboard.png)

### 📊 Match Results
![Match Results](images/match_results.png)

### 🔍 Comparison View
![Comparison View](images/comparison_view.png)

### 🌍 Map View
![Map](images/map.png)

\---



\## 🧠 Approach



The system performs multi-source record linkage using:



\- \*\*Fuzzy name matching\*\* (RapidFuzz)

\- \*\*Birth year comparison\*\*

\- \*\*Location/Community similarity\*\*



Each match is scored and classified into:



\- ✅ \*\*High Match\*\*

\- ⚠️ \*\*Possible Match\*\*

\- 🔴 \*\*Manual Review\*\*



Additionally, records are evaluated for:



\- \*\*Completeness\*\*

\- \*\*Missing values\*\*

\- \*\*Data consistency\*\*



\---



\## 🚀 Features



\- 🔍 Fuzzy record matching across datasets

\- 📊 Interactive dashboard with real-time metrics

\- 🧪 Data quality assessment and scoring

\- 🚨 Priority investigation case identification

\- 🔍 Side-by-side record comparison view

\- 📥 Export matched results (CSV download)

\- 🌍 Map visualization of records



\---



\## 📊 Dashboard Capabilities



The Streamlit app allows users to:



\- 🔍 Search and filter records

\- 📊 Analyze match categories and confidence scores

\- 🧪 Evaluate data quality and completeness

\- 🚨 Identify high-priority investigation cases

\- 📉 Visualize distributions of matches and quality metrics

\- 🔍 Compare matched records side-by-side



\---



\## 🛠️ Tech Stack



\- \*\*Python\*\*

\- \*\*Pandas\*\*

\- \*\*Streamlit\*\*

\- \*\*RapidFuzz\*\*



\---



\## ▶️ How to Run Locally



1\. Clone the repository:

```bash

git clone https://github.com/Godsbrain/Arctic\_Record\_Reconciliation.git

cd Arctic\_Record\_Reconciliation



