# ml_engine.py
import pandas as pd
from sklearn.ensemble import IsolationForest
from config import ML_CONTAMINATION_RATE

def train_and_detect_ml_anomalies(df):
    """
    Applies an unsupervised Isolation Forest model to flag complex, 
    multi-dimensional operational anomalies.
    """
    feature_cols = [
        "scheduled_hours", 
        "active_hours", 
        "idle_hours", 
        "billed_hours", 
        "hourly_rate", 
        "active_variance",
        "potential_financial_leakage"
    ]
    
    X = df[feature_cols].copy()
    
    # Initialize Isolation Forest Model
    model = IsolationForest(
        n_estimators=100, 
        contamination=ML_CONTAMINATION_RATE, 
        random_state=42
    )
    
    # Fit and predict: -1 indicates an anomaly, 1 indicates normal
    df["ml_raw_score"] = model.fit_predict(X)
    df["ml_anomaly_flag"] = df["ml_raw_score"].apply(lambda x: 1 if x == -1 else 0)
    
    return df