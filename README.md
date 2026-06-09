# 🖥️ IT Operations & Incident Intelligence Dashboard

## Project Overview
Analyzed 25,000+ IT operational logs and support ticket records using SQL and Python to identify recurring incident patterns and system performance trends. Built interactive dashboards tracking key IT operations KPIs.

---

## Tools & Technologies
| Tool | Usage |
|---|---|
| Python (Pandas, Matplotlib, Seaborn, Faker) | Data generation, cleaning, EDA, automation |
| PostgreSQL | Data storage and SQL analysis |
| Jupyter Notebook | Exploratory data analysis and charts |
| Power BI | Interactive KPI dashboards with DAX measures |
| Streamlit | Live web dashboard for real-time filtering |

---

## Project Structure
```
IT-Ops-Dashboard/
│
├── data/
│   ├── incident_tickets.csv       ← 25,000 ticket records
│   ├── system_logs.csv            ← 25,000 system log records
│   ├── chart1_category.png        ← Tickets by category
│   ├── chart2_monthly.png         ← Monthly ticket trend
│   ├── chart3_mttr.png            ← Resolution time by priority
│   ├── chart4_escalation.png      ← Escalation rate by team
│   └── kpi_report.xlsx            ← Auto-generated KPI report
│
├── sql/
│   ├── 01_avg_resolution.sql      ← Avg resolution time by category
│   ├── 02_tickets_by_team.sql     ← Ticket count by team
│   ├── 03_escalation_rate.sql     ← Escalation rate by team
│   ├── 04_monthly_trend.sql       ← Monthly ticket volume
│   └── 05_server_performance.sql  ← Server uptime and response time
│
├── python/
│   ├── generate_data.py           ← Generates 25K rows of data
│   ├── load_to_postgres_fast.py   ← Loads data into PostgreSQL
│   ├── eda_analysis.ipynb         ← EDA notebook with 4 charts
│   └── app.py                     ← Streamlit live dashboard
│
├── powerbi/
│   └── IT_Ops_Dashboard.pbix      ← Power BI dashboard file
│
├── requirements.txt               ← All required libraries
└── README.md                      ← Project documentation
```

---

## Key KPIs Tracked
- **MTTR** — Mean Time To Resolve incidents
- **Escalation Rate** — Percentage of tickets escalated per team
- **Resolution Rate** — Percentage of tickets resolved
- **Uptime %** — Average server uptime percentage
- **Ticket Volume** — Monthly and category-wise ticket trends

---

## Key Findings
- Software category has the highest ticket volume
- P1 priority tickets have the longest average resolution time
- Escalation rate varies significantly across teams
- Server uptime remains consistently above 92% across all servers
- Ticket volume shows consistent monthly distribution over the year

---

## SQL Queries
5 queries written in PostgreSQL covering:
- GROUP BY and aggregate functions (AVG, COUNT, SUM)
- Percentage calculations for escalation rate
- Date formatting with TO_CHAR for monthly trends
- Index optimization for query performance

---

## Python EDA
- Loaded and cleaned 25,000+ records using Pandas
- Fixed date columns using pd.to_datetime()
- Created 4 visualizations using Matplotlib and Seaborn
- Automated weekly KPI report export to Excel using openpyxl
- Reduced manual reporting effort by approximately 30%

---

## Power BI Dashboards
3 interactive dashboard pages with filters and slicers:

**Page 1 — KPI Overview**
- Total tickets, MTTR, escalation rate, resolution rate cards
- Donut chart by category
- Bar chart by team

**Page 2 — Trends**
- Monthly ticket volume line chart
- Tickets by priority bar chart
- Avg resolution time by category

**Page 3 — Team Performance**
- Escalation rate by team
- Resolution time by team
- Full team summary table

### DAX Measures Used
```
MTTR = AVERAGE(incident_tickets[resolution_time_hrs])

Escalation Rate = 
DIVIDE(
    COUNTROWS(FILTER(incident_tickets, incident_tickets[is_escalated] = 1)),
    COUNTROWS(incident_tickets)
) * 100

Resolution Rate = 
DIVIDE(
    COUNTROWS(FILTER(incident_tickets, incident_tickets[status] = "Resolved")),
    COUNTROWS(incident_tickets)
) * 100
```

---

## Live Dashboard (Streamlit)
Run the live interactive dashboard locally:

```bash
pip install -r requirements.txt
python -m streamlit run python/app.py
```

Opens at: `http://localhost:8501`

Features:
- Filter by category, team, and priority
- KPI cards update in real time
- 6 interactive Plotly charts
- Server performance section

---

## How to Run This Project

**Step 1 — Install libraries**
```bash
pip install -r requirements.txt
```

**Step 2 — Generate data**
```bash
python python/generate_data.py
```

**Step 3 — Load into PostgreSQL**
```bash
python python/load_to_postgres_fast.py
```

**Step 4 — Run EDA notebook**
```
Open python/eda_analysis.ipynb in VS Code
Run all cells with Shift + Enter
```

**Step 5 — Run live dashboard**
```bash
python -m streamlit run python/app.py
```

---

## Author
- **Name:** Your Name
- **LinkedIn:** your-linkedin-link
- **Email:** your-email
