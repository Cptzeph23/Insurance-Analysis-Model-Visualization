import pandas as pd
from sklearn.ensemble import IsolationForest


def detect_anomalies(df):
    features = df[
        ["premium", "comm", "outstanding", "policy_net", "credit_net"]
    ].fillna(0)

    model = IsolationForest(
        contamination=0.02,
        random_state=42
    )

    df["anomaly_flag"] = model.fit_predict(features)
    df["anomaly_flag"] = df["anomaly_flag"].map({1: 0, -1: 1})

    df["risk_score"] = model.decision_function(features) * -1

    return df


