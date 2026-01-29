import streamlit as st
from data_loader import load_data
from kpis import compute_kpis
from forecast import build_forecast
from charts import forecast_chart



from charts import (
    revenue_trend_chart,
    top_customers_chart,
    outstanding_distribution_chart,
    outstanding_vs_premium_scatter,
    customer_distribution_chart
)


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
# Global Filters
# -----------------------
st.sidebar.subheader("Filters")

# Date Filter
if "issue_date" in df.columns:
    min_date = df["issue_date"].min()
    max_date = df["issue_date"].max()

    date_range = st.sidebar.date_input(
        "Issue Date Range",
        value=(min_date, max_date)
    )

    if len(date_range) == 2:
        start_date, end_date = date_range
        df = df[
            (df["issue_date"] >= str(start_date)) &
            (df["issue_date"] <= str(end_date))
        ]

# Customer Filter
customers = sorted(df["insured"].dropna().unique())
selected_customers = st.sidebar.multiselect(
    "Select Customer(s)",
    customers,
    default=customers
)

df = df[df["insured"].isin(selected_customers)]

# Risk Filter
risk_filter = st.sidebar.selectbox(
    "Risk Level",
    ["All", "High Risk Only", "Low Risk Only"]
)

if risk_filter == "High Risk Only":
    df = df[df["risk_flag"] == True]
elif risk_filter == "Low Risk Only":
    df = df[df["risk_flag"] == False]

# Outstanding Bucket Filter
if "outstanding_bucket" in df.columns:
    buckets = df["outstanding_bucket"].dropna().unique().tolist()
    selected_bucket = st.sidebar.multiselect(
        "Outstanding Bucket",
        buckets,
        default=buckets
    )
    df = df[df["outstanding_bucket"].isin(selected_bucket)]

# Recompute KPIs after filtering
kpis = compute_kpis(df)



# -----------------------
# Sidebar Navigation
# -----------------------

st.sidebar.markdown("##  Insurance Analytics")
st.sidebar.markdown("Interactive Business Intelligence Dashboard")

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
    st.title(" Executive Overview")

    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Premium", f"{kpis['total_premium']:,.0f}")
    col2.metric("Net Revenue", f"{kpis['net_revenue']:,.0f}")
    col3.metric("Outstanding", f"{kpis['total_outstanding']:,.0f}")
    col4.metric("Outstanding %", f"{kpis['outstanding_ratio']:.1%}")

    st.divider()

    st.plotly_chart(revenue_trend_chart(df), use_container_width=True)

    colA, colB = st.columns(2)
    colA.plotly_chart(top_customers_chart(df), use_container_width=True)
    colB.plotly_chart(outstanding_distribution_chart(df), use_container_width=True)

    # Forecast Section
    forecast, model = build_forecast(df)
    st.plotly_chart(forecast_chart(forecast), use_container_width=True)



elif page == "Risk & Audit":
    st.title(" Risk & Audit Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric("High Risk Accounts", kpis["high_risk_count"])
    col2.metric("High Risk Outstanding", f"{kpis['high_risk_outstanding']:,.0f}")
    col3.metric("Risk Policy Ratio", f"{kpis['risk_policy_ratio']:.1%}")

    st.divider()

    st.plotly_chart(outstanding_vs_premium_scatter(df), use_container_width=True)

    st.subheader("High Risk Policies")
    st.dataframe(df[df["risk_flag"] == True])


elif page == "Customer Intelligence":
    st.title(" Customer Intelligence")

    col1, col2 = st.columns(2)
    col1.metric("Active Customers", kpis["active_customers"])
    col2.metric("Avg Premium", f"{kpis['avg_premium']:,.0f}")

    st.divider()

    st.plotly_chart(customer_distribution_chart(df), use_container_width=True)

    st.subheader("Top Customers")
    top_customers = (
        df.groupby("insured")["premium"]
        .sum()
        .sort_values(ascending=False)
        .head(20)
        .reset_index()
    )

    st.dataframe(top_customers)
