import pandas as pd
import random
from faker import Faker
import os

fake = Faker()
random.seed(42)

os.makedirs("../data", exist_ok=True)

print("Starting data generation...")

categories = ["Network", "Hardware", "Software", "Security"]
priorities  = ["P1", "P2", "P3", "P4"]
teams       = ["Team A", "Team B", "Team C", "Team D"]
statuses    = ["Resolved", "Escalated", "Open"]
servers     = ["Server-A", "Server-B", "Server-C", "Server-D", "Server-E"]
log_levels  = ["INFO", "WARN", "ERROR", "CRITICAL"]   # ← add this line

tickets = []
for i in range(25000):
    tickets.append({
        "ticket_id":           f"TKT-{i+1}",
        "created_date":        fake.date_between(start_date="-1y", end_date="today"),
        "category":            random.choice(categories),
        "priority":            random.choice(priorities),
        "assigned_team":       random.choice(teams),
        "status":              random.choice(statuses),
        "resolution_time_hrs": round(random.uniform(1, 72), 2),
        "is_escalated":        random.choice([0, 0, 0, 1]),
        "server_id":           random.choice(servers)    # ← new column added
    })

df_tickets = pd.DataFrame(tickets)
df_tickets.to_csv("../data/incident_tickets.csv", index=False)
print("✓ incident_tickets.csv saved —", len(df_tickets), "rows")

logs = []
for i in range(25000):
    logs.append({
        "log_id":            f"LOG-{i+1}",
        "timestamp":         fake.date_time_between(start_date="-1y", end_date="now"),
        "server_id":         random.choice(servers),
        "log_level":         random.choice(log_levels),
        "uptime_percentage": round(random.uniform(85, 100), 2),
        "response_time_ms":  round(random.uniform(50, 2000), 2)
    })

df_logs = pd.DataFrame(logs)
df_logs.to_csv("../data/system_logs.csv", index=False)
print("✓ system_logs.csv saved —", len(df_logs), "rows")

print("\nDone! Check your data/ folder.")