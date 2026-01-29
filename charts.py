import plotly.express as px


# -----------------------------
# Executive Charts
# -----------------------------

def revenue_trend_chart(df):
    monthly = (
        df.groupby("year_month")["premium"]
        .sum()
        .reset_index()
        .sort_values("year_month")
    )

    fig = px.line(
        monthly,
        x="year_month",
        y="premium",
        title="Monthly Premium Trend",
        markers=True
    )

    return fig


def top_customers_chart(df, top_n=10):
    top = (
        df.groupby("insured")["premium"]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )

    fig = px.bar(
        top,
        x="premium",
        y="insured",
        orientation="h",
        title="Top Customers by Premium"
    )

    return fig


def outstanding_distribution_chart(df):
    bucket = (
        df["outstanding_bucket"]
        .value_counts()
        .reset_index()
    )
    bucket.columns = ["bucket", "count"]

    fig = px.pie(
        bucket,
        names="bucket",
        values="count",
        title="Outstanding Distribution"
    )

    return fig


# -----------------------------
# Risk Charts
# -----------------------------

def outstanding_vs_premium_scatter(df):
    fig = px.scatter(
        df,
        x="premium",
        y="outstanding",
        color="risk_flag",
        hover_data=["insured", "policy_net"],
        title="Outstanding vs Premium (Risk View)"
    )

    return fig


# -----------------------------
# Customer Intelligence Charts
# -----------------------------

def customer_distribution_chart(df):
    cust = (
        df.groupby("insured")["premium"]
        .sum()
        .reset_index()
    )

    fig = px.histogram(
        cust,
        x="premium",
        nbins=30,
        title="Customer Premium Distribution"
    )

    return fig
