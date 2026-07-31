# reconciliation.py
import pandas as pd

def fetch_reconciliation_matrix(conn):
    query = """
    SELECT 
        s.shift_date,
        s.account_id,
        s.agent_id,
        s.scheduled_hours,
        COALESCE(l.active_hours, 0) AS active_hours,
        COALESCE(l.idle_hours, 0) AS idle_hours,
        COALESCE(b.billed_hours, 0) AS billed_hours,
        COALESCE(b.hourly_rate, 0) AS hourly_rate,
        (COALESCE(b.billed_hours, 0) - s.scheduled_hours) AS schedule_variance,
        (COALESCE(b.billed_hours, 0) - COALESCE(l.active_hours, 0)) AS active_variance,
        ((COALESCE(b.billed_hours, 0) - COALESCE(l.active_hours, 0)) * COALESCE(b.hourly_rate, 0)) AS potential_financial_leakage
    FROM scheduled_shifts s
    LEFT JOIN system_logins l 
        ON s.agent_id = l.agent_id AND s.shift_date = l.shift_date
    LEFT JOIN client_billing b 
        ON s.agent_id = b.agent_id AND s.shift_date = b.shift_date
    """
    df = pd.read_sql_query(query, conn)
    return df