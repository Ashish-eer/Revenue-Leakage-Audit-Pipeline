# audit_rules.py
import pandas as pd
from config import Z_SCORE_THRESHOLD, MAX_IDLE_HOURS_THRESHOLD, UNBILLED_WORK_TOLERANCE_HOURS
from ml_engine import train_and_detect_ml_anomalies

def evaluate_audit_logic(df):
    # 1. Statistical Z-Score Calculation
    mean_leakage = df["potential_financial_leakage"].mean()
    std_leakage = df["potential_financial_leakage"].std()

    if std_leakage == 0 or pd.isna(std_leakage):
        df["z_score"] = 0.0
    else:
        df["z_score"] = (df["potential_financial_leakage"] - mean_leakage) / std_leakage

    # 2. Run Unsupervised ML Anomaly Detection Engine
    df = train_and_detect_ml_anomalies(df)

    # 3. Hybrid Flag Evaluation (Rules + Z-Score + ML)
    def apply_rules(row):
        flags = []
        if row["active_hours"] == 0 and row["billed_hours"] > 0:
            flags.append("GHOST_BILLING")
        if row["billed_hours"] < (row["active_hours"] - UNBILLED_WORK_TOLERANCE_HOURS):
            flags.append("UNBILLED_WORK")
        if row["idle_hours"] > MAX_IDLE_HOURS_THRESHOLD:
            flags.append("EXCESSIVE_IDLE")
        if abs(row["z_score"]) >= Z_SCORE_THRESHOLD:
            flags.append("STATISTICAL_OUTLIER")
        if row["ml_anomaly_flag"] == 1:
            flags.append("ML_PATTERN_ANOMALY")

        return "|".join(flags) if flags else "CLEAN"

    df["audit_flag"] = df.apply(apply_rules, axis=1)
    df["is_anomaly"] = df["audit_flag"].apply(lambda x: 1 if x != "CLEAN" else 0)
    
    return df