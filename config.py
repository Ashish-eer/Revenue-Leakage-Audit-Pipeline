# config.py

# Database Configuration
DB_NAME = "audit_database.db"

# Audit Thresholds
Z_SCORE_THRESHOLD = 2.5
MAX_IDLE_HOURS_THRESHOLD = 4.0
UNBILLED_WORK_TOLERANCE_HOURS = 2.0

# Machine Learning Parameters
ML_CONTAMINATION_RATE = 0.05  # Expected percentage of anomalies (5%)

# Report & API Configurations
OUTPUT_REPORT_NAME = "Revenue_Leakage_Audit_Report.xlsx"
GOOGLE_SERVICE_ACCOUNT_FILE = "credentials.json"  # Path to Google Service Account Key
GOOGLE_SHEET_NAME = "Enterprise Revenue Leakage Audit Dashboard"