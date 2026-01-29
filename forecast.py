import pandas as pd
from prophet import Prophet


def build_forecast(df, periods=12):
    """
    Builds monthly premium forecast.
    """
    monthly = (
        df.groupby("year_month")["premium"]
        .sum()
        .reset_index()
        .rename(columns={
            "year_month": "ds",
            "premium": "y"
        })
    )

    monthly["ds"] = pd.to_datetime(monthly["ds"])

    model = Prophet()
    model.fit(monthly)

    future = model.make_future_dataframe(periods=periods, freq="M")
    forecast = model.predict(future)

    return forecast, model
