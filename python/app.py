import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Config ---
st.set_page_config(
    page_title="IT Operations Dashboard",
    page_icon="🖥️",
    layout="wide"
)

# --- Load Data ---
df_tickets = pd.read_csv("../data/incident_tickets.csv")
df_logs    = pd.read_csv("../data/system_logs.csv")

# --- Clean Data ---
df_tickets["created_date"] = pd.to_datetime(df_tickets["created_date"])
df_tickets["month"]        = df_tickets["created_date"].dt.to_period("M").astype(str)

# --- Sidebar ---
st.sidebar.title("🔍 Filters")

# Category filter
categories = ["All"] + list(df_tickets["category"].unique())
selected_category = st.sidebar.selectbox("Select Category", categories)

# Team filter
teams = ["All"] + list(df_tickets["assigned_team"].unique())
selected_team = st.sidebar.selectbox("Select Team", teams)

# Priority filter
priorities = ["All"] + list(df_tickets["priority"].unique())
selected_priority = st.sidebar.selectbox("Select Priority", priorities)

# --- Apply Filters ---
filtered = df_tickets.copy()

if selected_category != "All":
    filtered = filtered[filtered["category"] == selected_category]

if selected_team != "All":
    filtered = filtered[filtered["assigned_team"] == selected_team]

if selected_priority != "All":
    filtered = filtered[filtered["priority"] == selected_priority]

# --- Title ---
st.title("🖥️ IT Operations & Incident Intelligence Dashboard")
st.markdown("---")

# ================================
# PAGE 1 — KPI CARDS
# ================================
st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Tickets",
        value=len(filtered)
    )

with col2:
    mttr = round(filtered["resolution_time_hrs"].mean(), 2)
    st.metric(
        label="Avg MTTR (hrs)",
        value=mttr
    )

with col3:
    escalation_rate = round(
        100 * filtered["is_escalated"].sum() / len(filtered), 1
    )
    st.metric(
        label="Escalation Rate %",
        value=f"{escalation_rate}%"
    )

with col4:
    resolution_rate = round(
        100 * len(filtered[filtered["status"] == "Resolved"]) / len(filtered), 1
    )
    st.metric(
        label="Resolution Rate %",
        value=f"{resolution_rate}%"
    )

st.markdown("---")

# ================================
# PAGE 2 — CHARTS
# ================================
st.subheader("📈 Trends & Analysis")

# Row 1 — two charts side by side
col1, col2 = st.columns(2)

with col1:
    # Bar chart — tickets by category
    cat_data = filtered["category"].value_counts().reset_index()
    cat_data.columns = ["category", "count"]
    fig1 = px.bar(
        cat_data,
        x="category",
        y="count",
        title="Tickets by Category",
        color="category"
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # Pie chart — tickets by priority
    pri_data = filtered["priority"].value_counts().reset_index()
    pri_data.columns = ["priority", "count"]
    fig2 = px.pie(
        pri_data,
        names="priority",
        values="count",
        title="Tickets by Priority"
    )
    st.plotly_chart(fig2, use_container_width=True)

# Row 2 — monthly trend full width
monthly = filtered.groupby("month")["ticket_id"].count().reset_index()
monthly.columns = ["month", "count"]
fig3 = px.line(
    monthly,
    x="month",
    y="count",
    title="Monthly Ticket Volume Trend",
    markers=True
)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# ================================
# PAGE 3 — TEAM PERFORMANCE
# ================================
st.subheader("👥 Team Performance")

col1, col2 = st.columns(2)

with col1:
    # Escalation rate by team
    team_data = filtered.groupby("assigned_team").agg(
        total=("ticket_id", "count"),
        escalated=("is_escalated", "sum")
    ).reset_index()
    team_data["escalation_pct"] = round(
        100 * team_data["escalated"] / team_data["total"], 1
    )
    fig4 = px.bar(
        team_data,
        x="assigned_team",
        y="escalation_pct",
        title="Escalation Rate by Team %",
        color="assigned_team"
    )
    st.plotly_chart(fig4, use_container_width=True)

with col2:
    # Avg resolution time by team
    res_data = filtered.groupby("assigned_team").agg(
        avg_resolution=("resolution_time_hrs", "mean")
    ).reset_index()
    res_data["avg_resolution"] = res_data["avg_resolution"].round(2)
    fig5 = px.bar(
        res_data,
        x="assigned_team",
        y="avg_resolution",
        title="Avg Resolution Time by Team (hrs)",
        color="assigned_team"
    )
    st.plotly_chart(fig5, use_container_width=True)

# Summary table
st.subheader("📋 Full Team Summary Table")
summary = filtered.groupby("assigned_team").agg(
    total_tickets=("ticket_id", "count"),
    avg_resolution_hrs=("resolution_time_hrs", "mean"),
    escalation_count=("is_escalated", "sum"),
    resolved=("status", lambda x: (x == "Resolved").sum())
).round(2).reset_index()

st.dataframe(summary, use_container_width=True)

# ================================
# SERVER PERFORMANCE
# ================================
st.markdown("---")
st.subheader("🖥️ Server Performance")

server_data = df_logs.groupby("server_id").agg(
    avg_uptime=("uptime_percentage", "mean"),
    avg_response_ms=("response_time_ms", "mean"),
    total_logs=("log_id", "count")
).round(1).reset_index()

fig6 = px.bar(
    server_data,
    x="server_id",
    y="avg_uptime",
    title="Average Uptime % by Server",
    color="server_id"
)
st.plotly_chart(fig6, use_container_width=True)

st.dataframe(server_data, use_container_width=True)