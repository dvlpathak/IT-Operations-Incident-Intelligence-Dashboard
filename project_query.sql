-- Query 1: Average resolution time by category

SELECT category,
ROUND(AVG(resolution_time_hrs)::numeric,2) AS avg_hours,
COUNT(*) AS  total_tickets
FROM incident_tickets
GROUP BY category
ORDER BY avg_hours DESC;

-- Query 2: Ticket count by team

SELECT assigned_team, COUNT(*) AS ticket_count
FROM incident_tickets
GROUP BY assigned_team
ORDER BY ticket_count DESC;

-- Query 3: Escalation rate by team

SELECT assigned_team,
       COUNT(*) AS total,
       SUM(is_escalated) AS escalated,
       ROUND(100.0 * SUM(is_escalated) / COUNT(*), 1) AS escalation_pct
FROM incident_tickets
GROUP BY assigned_team
ORDER BY escalation_pct DESC;

-- Query 4: Monthly ticket volume
SELECT TO_CHAR(created_date, 'YYYY-MM') AS month,
       COUNT(*) AS tickets
FROM incident_tickets
GROUP BY month
ORDER BY month;

CREATE INDEX idx_logs_server ON system_logs(server_id);
CREATE INDEX idx_tickets_server ON incident_tickets(server_id);


-- Query 5: Join both tables

SELECT server_id,
       ROUND(AVG(uptime_percentage)::numeric, 1) AS avg_uptime,
       ROUND(AVG(response_time_ms)::numeric, 1)  AS avg_response_ms,
       COUNT(*) AS total_logs
FROM system_logs
GROUP BY server_id
ORDER BY avg_uptime ASC;


