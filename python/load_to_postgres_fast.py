import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# --- Connect ---
conn = psycopg2.connect(
    host     = "localhost",
    database = "it_ops_db",
    user     = "postgres",
    password = "pass123",      # change to your password
    port     = "5432"
)
cursor = conn.cursor()
print("✓ Connected to PostgreSQL")

# --- Load CSVs ---
df_tickets = pd.read_csv("../data/incident_tickets.csv")
df_logs    = pd.read_csv("../data/system_logs.csv")
print("✓ CSV files loaded")

# --- Create Tables ---
cursor.execute("""
    DROP TABLE IF EXISTS incident_tickets;
    CREATE TABLE incident_tickets (
        ticket_id           VARCHAR(20),
        created_date        DATE,
        category            VARCHAR(50),
        priority            VARCHAR(10),
        assigned_team       VARCHAR(50),
        status              VARCHAR(20),
        resolution_time_hrs FLOAT,
        is_escalated        INT,
        server_id           VARCHAR(20)
    );
""")

cursor.execute("""
    DROP TABLE IF EXISTS system_logs;
    CREATE TABLE system_logs (
        log_id             VARCHAR(20),
        timestamp          TIMESTAMP,
        server_id          VARCHAR(20),
        log_level          VARCHAR(20),
        uptime_percentage  FLOAT,
        response_time_ms   FLOAT
    );
""")
print("✓ Tables created")

# --- Insert tickets ---
ticket_rows = list(df_tickets.itertuples(index=False, name=None))
execute_values(cursor, """
    INSERT INTO incident_tickets VALUES %s
""", ticket_rows)
print("✓ incident_tickets inserted —", len(ticket_rows), "rows")

# --- Insert logs ---
log_rows = list(df_logs.itertuples(index=False, name=None))
execute_values(cursor, """
    INSERT INTO system_logs VALUES %s
""", log_rows)
print("✓ system_logs inserted —", len(log_rows), "rows")

# --- Save and close ---
conn.commit()
cursor.close()
conn.close()
print("\nAll done! Open pgAdmin and check your tables.")