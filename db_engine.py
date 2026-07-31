# db_engine.py
import sqlite3
import numpy as np
from datetime import datetime, timedelta
from config import DB_NAME

def get_connection(db_path=DB_NAME):
    return sqlite3.connect(db_path)

def initialize_database(conn):
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scheduled_shifts (
        shift_id TEXT PRIMARY KEY,
        agent_id TEXT,
        account_id TEXT,
        shift_date DATE,
        scheduled_hours REAL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS system_logins (
        login_id TEXT PRIMARY KEY,
        agent_id TEXT,
        shift_date DATE,
        active_hours REAL,
        idle_hours REAL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS client_billing (
        billing_id TEXT PRIMARY KEY,
        agent_id TEXT,
        account_id TEXT,
        shift_date DATE,
        billed_hours REAL,
        hourly_rate REAL
    );
    """)
    conn.commit()

def seed_synthetic_data(conn, num_records=1000, seed=42):
    np.random.seed(seed)
    cursor = conn.cursor()

    # Clear existing records
    cursor.execute("DELETE FROM scheduled_shifts;")
    cursor.execute("DELETE FROM system_logins;")
    cursor.execute("DELETE FROM client_billing;")

    agents = [f"AGT_{1000 + i}" for i in range(50)]
    accounts = [f"ACC_{100 + i}" for i in range(10)]
    start_date = datetime(2026, 7, 1)

    shifts_data = []
    logins_data = []
    billing_data = []

    for i in range(num_records):
        agent = np.random.choice(agents)
        account = np.random.choice(accounts)
        shift_date = (start_date + timedelta(days=int(i % 30))).strftime("%Y-%m-%d")

        sched_hrs = 8.0
        rand_val = np.random.rand()

        if rand_val < 0.82:
            # Standard Clean Operational Shift
            active_hrs = np.random.normal(7.5, 0.2)
            idle_hrs = 8.0 - active_hrs
            billed_hrs = 8.0
        elif rand_val < 0.88:
            # Anomaly Type 1: Ghost Billing (No system login, full billing)
            active_hrs = 0.0
            idle_hrs = 0.0
            billed_hrs = 8.0
        elif rand_val < 0.94:
            # Anomaly Type 2: Unbilled Work (High active work, suppressed billing)
            active_hrs = 8.5
            idle_hrs = 0.5
            billed_hrs = 4.0
        else:
            # Anomaly Type 3: Excessive Inactivity / Idle Time
            active_hrs = 2.5
            idle_hrs = 5.5
            billed_hrs = 8.0

        rate = np.random.choice([20.00, 25.00, 32.00, 45.00])

        shifts_data.append((f"SHF_{i:05d}", agent, account, shift_date, sched_hrs))
        logins_data.append((f"LOG_{i:05d}", agent, shift_date, round(max(0, active_hrs), 2), round(max(0, idle_hrs), 2)))
        billing_data.append((f"BIL_{i:05d}", agent, account, shift_date, round(max(0, billed_hrs), 2), rate))

    cursor.executemany("INSERT INTO scheduled_shifts VALUES (?, ?, ?, ?, ?)", shifts_data)
    cursor.executemany("INSERT INTO system_logins VALUES (?, ?, ?, ?, ?)", logins_data)
    cursor.executemany("INSERT INTO client_billing VALUES (?, ?, ?, ?, ?, ?)", billing_data)
    conn.commit()