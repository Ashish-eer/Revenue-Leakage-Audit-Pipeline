# main.py
import time
from db_engine import get_connection, initialize_database, seed_synthetic_data
from reconciliation import fetch_reconciliation_matrix
from audit_rules import evaluate_audit_logic
from report_generator import generate_excel_report
from gsheets_exporter import export_to_google_sheets
from config import OUTPUT_REPORT_NAME

def run_pipeline():
    start_time = time.time()
    print("==================================================")
    print(" ENTERPRISE REVENUE LEAKAGE AUDIT PIPELINE ")
    print("==================================================")

    print("\n[1/5] Connecting to Database & Initializing Schema...")
    conn = get_connection()
    initialize_database(conn)
    seed_synthetic_data(conn, num_records=1000)

    print("[2/5] Running Multi-Source SQL Reconciliation Engine...")
    raw_df = fetch_reconciliation_matrix(conn)
    print(f"      Successfully extracted {len(raw_df)} reconciled records.")

    print("[3/5] Applying Rules, Z-Scores & ML Anomaly Detection...")
    audited_df = evaluate_audit_logic(raw_df)
    anomalies_found = audited_df["is_anomaly"].sum()
    ml_anomalies = audited_df["ml_anomaly_flag"].sum()
    print(f"      Audit finished. Flagged {anomalies_found} total anomalies ({ml_anomalies} via ML Isolation Forest).")

    print("[4/5] Rendering Formatted Local Excel Audit Report...")
    generate_excel_report(audited_df, OUTPUT_REPORT_NAME)

    print("[5/5] Executing Cloud Sync to Google Sheets Dashboard...")
    export_to_google_sheets(audited_df)

    conn.close()
    elapsed = round(time.time() - start_time, 2)
    print(f"\n[SUCCESS] Pipeline executed successfully in {elapsed}s.")
    print(f"[OUTPUT] Local Excel: {OUTPUT_REPORT_NAME}")
    print("==================================================")

if __name__ == "__main__":
    run_pipeline()