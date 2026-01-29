import pandas as pd


def compute_kpis(df: pd.DataFrame) -> dict:
    kpis = {}

    # ------------------------
    # Executive KPIs
    # ------------------------
    kpis["total_premium"] = df["premium"].sum()
    kpis["net_revenue"] = df["policy_net"].sum()
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
    high_risk_df = df[df["risk_flag"] == True]

    kpis["high_risk_count"] = len(high_risk_df)
    kpis["high_risk_outstanding"] = high_risk_df["outstanding"].sum()
    kpis["risk_policy_ratio"] = (
        len(high_risk_df) / len(df) if len(df) else 0
    )

    # ------------------------
    # Operational KPIs
    # ------------------------
    monthly = (
        df.groupby("year_month")["premium"]
        .sum()
        .sort_index()
    )

    if len(monthly) > 1:
        kpis["latest_month_growth"] = (
            monthly.iloc[-1] - monthly.iloc[-2]
        ) / max(monthly.iloc[-2], 1)
    else:
        kpis["latest_month_growth"] = 0

    return kpis
