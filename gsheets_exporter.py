# gsheets_exporter.py
import os
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from config import GOOGLE_SERVICE_ACCOUNT_FILE, GOOGLE_SHEET_NAME

def export_to_google_sheets(df):
    """
    Syncs the audit executive summary and anomaly records to Google Sheets.
    If credentials.json is absent, it skips gracefully without crashing the pipeline.
    """
    if not os.path.exists(GOOGLE_SERVICE_ACCOUNT_FILE):
        print("      [SKIP] 'credentials.json' not found. Skipping Google Sheets cloud sync.")
        return

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    try:
        credentials = Credentials.from_service_account_file(
            GOOGLE_SERVICE_ACCOUNT_FILE, 
            scopes=scopes
        )
        gc = gspread.authorize(credentials)

        # Open existing sheet or create new one
        try:
            sh = gc.open(GOOGLE_SHEET_NAME)
        except gspread.exceptions.SpreadsheetNotFound:
            sh = gc.create(GOOGLE_SHEET_NAME)

        # Tab 1: Flagged Anomalies Only
        anomalies_df = df[df["is_anomaly"] == 1].copy()
        
        # Format dates/floats for JSON compatibility
        anomalies_df = anomalies_df.astype(str)

        try:
            worksheet = sh.worksheet("Flagged Anomalies")
            worksheet.clear()
        except gspread.exceptions.WorksheetNotFound:
            worksheet = sh.add_worksheet(title="Flagged Anomalies", rows="1000", cols="20")

        # Push data
        data_to_push = [anomalies_df.columns.values.tolist()] + anomalies_df.values.tolist()
        worksheet.update(data_to_push)
        print(f"      [SUCCESS] Synced {len(anomalies_df)} anomalies directly to Google Sheets!")

    except Exception as e:
        print(f"      [WARNING] Google Sheets Export Failed: {str(e)}")