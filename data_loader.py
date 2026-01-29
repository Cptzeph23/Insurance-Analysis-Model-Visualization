import pandas as pd
import streamlit as st


@st.cache_data
def load_data():
    """
    Loads and preprocesses insurance dataset.
    Cached for performance.
    """
    df = pd.read_csv("data/insurance.csv")

    # -----------------------------
    # Standardize column names
    # -----------------------------
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # -----------------------------
    # Parse dates safely
    # -----------------------------
    date_cols = [col for col in df.columns if "date" in col]

    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    # -----------------------------
    # Ensure numeric columns
    # -----------------------------
    numeric_cols = [
        "premium",
        "outstanding",
        "net_revenue"
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # -----------------------------
    # Feature engineering
    # -----------------------------
    if "policy_date" in df.columns:
        df["year"] = df["policy_date"].dt.year
        df["month"] = df["policy_date"].dt.to_period("M").astype(str)

    # Risk flag
    if {"premium", "outstanding"}.issubset(df.columns):
        df["risk_flag"] = df["outstanding"] > (0.3 * df["premium"])

    # Outstanding bucket
    if "outstanding" in df.columns:
        df["outstanding_bucket"] = pd.cut(
            df["outstanding"],
            bins=[-1, 0, 10000, 50000, float("inf")],
            labels=["Zero", "Low", "Medium", "High"]
        )

    return df



