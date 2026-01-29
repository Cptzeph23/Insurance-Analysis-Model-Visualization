import pandas as pd
from io import BytesIO


def export_excel(kpis, forecast_df, anomaly_df):
    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        pd.DataFrame([kpis]).to_excel(writer, sheet_name="KPIs", index=False)
        forecast_df.to_excel(writer, sheet_name="Forecast", index=False)
        anomaly_df.to_excel(writer, sheet_name="Anomalies", index=False)

    return output.getvalue()
