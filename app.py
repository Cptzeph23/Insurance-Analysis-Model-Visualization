import streamlit as st
from data_loader import load_data
from kpis import compute_kpis

# -----------------------
# App Config
# -----------------------
st.set_page_config(
    page_title="Insurance Analytics Dashboard",
    layout="wide"
)

# -----------------------
# Load Data
# -----------------------
df = load_data()
kpis = compute_kpis(df)

# -----------------------
# Sidebar Navigation
# -----------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select Page",
    [
        "Executive Overview",
        "Risk & Audit",
        "Customer Intelligence"
    ]
)

# -----------------------
# Page Router
# -----------------------
if page == "Executive Overview":
    st.title("📊 Executive Overview")
    st.write("High-level business performance snapshot.")

    st.subheader("KPI Snapshot")
    st.json(kpis)

elif page == "Risk & Audit":
    st.title("⚠️ Risk & Audit Dashboard")
    st.write("Exposure, anomalies and financial risk monitoring.")

    st.subheader("Risk KPIs")
    st.json({
        "High Risk Accounts": kpis["high_risk_count"],
        "High Risk Outstanding": kpis["high_risk_outstanding"],
        "Risk Policy Ratio": kpis["risk_policy_ratio"]
    })

elif page == "Customer Intelligence":
    st.title("🧠 Customer Intelligence")
    st.write("Customer segmentation and performance insights.")

    st.subheader("Customer KPIs")
    st.json({
        "Active Customers": kpis["active_customers"],
        "Average Premium": kpis["avg_premium"]
    })
