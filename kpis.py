import pandas as pd


def compute_kpis(df: pd.DataFrame) -> dict:
    """
    Computes executive, risk, and operational KPIs.
    Returns dictionary of metrics.
    """

    kpis = {}

    # ------------------------
    # Executive KPIs
    # ------------------------
    kpis["total_premium"] = df["premium"].sum()
    kpis["net_revenue"] = df["net_revenue"].sum()
    kpis["total_outstanding"] = df["outstanding"].sum()

    kpis["active_customers"] = df["insured"].nunique()
    kpis["policy_count"] = len(df)

    if kpis["total_premium"] > 0:
        kpis["outstanding_ratio"] = (
            kpis["total_outstanding"] / kpis["total_premium"]
        )
    else:
        kpis["outstanding_ratio"] = 0

    kpis["avg_premium"] = df["premium"].mean()

    # ------------------------
    # Risk KPIs
    # ------------------------
    if "risk_flag" in df.columns:
        high_risk_df = df[df["risk_flag"] == True]
    else:
        high_risk_df = df[df["outstanding"] > 0]

    kpis["high_risk_count"] = len(high_risk_df)
    kpis["high_risk_outstanding"] = high_risk_df["outstanding"].sum()

    if len(df) > 0:
        kpis["risk_policy_ratio"] = len(high_risk_df) / len(df)
    else:
        kpis["risk_policy_ratio"] = 0

    # ------------------------
    # Operational KPIs
    # ------------------------
    if "month" in df.columns:
        monthly = (
            df.groupby("month")["premium"]
            .sum()
            .sort_index()
        )

        if len(monthly) > 1:
            kpis["latest_month_growth"] = (
                monthly.iloc
