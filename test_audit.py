# test_audit.py
import pytest
import pandas as pd
import sqlite3
from db_engine import initialize_database
from reconciliation import fetch_reconciliation_matrix
from audit_rules import evaluate_audit_logic

@pytest.fixture
def memory_db():
    conn = sqlite3.connect(":memory:")
    initialize_database(conn)
    cursor = conn.cursor()
    
    # Inject 1 Ghost Billing Row
    cursor.execute("INSERT INTO scheduled_shifts VALUES ('S1', 'A1', 'ACC1', '2026-07-01', 8.0);")
    cursor.execute("INSERT INTO system_logins VALUES ('L1', 'A1', '2026-07-01', 0.0, 0.0);")
    cursor.execute("INSERT INTO client_billing VALUES ('B1', 'A1', 'ACC1', '2026-07-01', 8.0, 25.0);")
    
    conn.commit()
    yield conn
    conn.close()

def test_ghost_billing_detection(memory_db):
    raw_df = fetch_reconciliation_matrix(memory_db)
    audited_df = evaluate_audit_logic(raw_df)
    
    assert len(audited_df) == 1
    assert "GHOST_BILLING" in audited_df.iloc[0]["audit_flag"]
    assert audited_df.iloc[0]["potential_financial_leakage"] == 200.00