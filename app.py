import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Russia-Ukraine War Analysis Dashboard",
    layout="wide"
)

# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv(
    r'data/CREA_of_PYHTON_SQL_READY.csv'
)

df["date"] = pd.to_datetime(df["date"])

# ==========================================
# TITLE
# ==========================================

st.title("🇺🇦 Russia-Ukraine War Analysis Dashboard")
st.markdown(
    "Interactive dashboard for analyzing personnel and equipment losses during the Russia-Ukraine conflict."
)

# ==========================================
# FRIENDLY COLUMN NAMES
# ==========================================

friendly_names = {
    "personnel": "Personnel Losses",
    "aircraft": "Aircraft Losses",
    "helicopter": "Helicopter Losses",
    "tank": "Tank Losses",
    "apc": "Armored Vehicle Losses",
    "field artillery": "Field Artillery Losses",
    "mrl": "Multiple Rocket Launcher Losses",
    "drone": "Drone Losses",
    "naval ship": "Naval Ship Losses",
    "anti-aircraft warfare": "Anti-Aircraft Warfare Losses",
    "special equipment": "Special Equipment Losses",
    "cruise missiles": "Cruise Missile Losses"
}

# ==========================================
# SIDEBAR
# ==========================================



metric_options = [
    "personnel",
    "tank",
    "aircraft",
    "helicopter",
    "apc",
    "field artillery",
    "drone",
    "cruise missiles"
]

selected_metric = st.selectbox(
    "Loss Categories",
    metric_options,
    format_func=lambda x: friendly_names.get(x, x)
)

# ==========================================
# KPI CARDS
# ==========================================

st.subheader(" Key Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Personnel Losses",
        f"{int(df['personnel'].max()):,}"
    )

with col2:
    st.metric(
        "Tank Losses",
        f"{int(df['tank'].max()):,}"
    )

with col3:
    st.metric(
        "Aircraft Losses",
        f"{int(df['aircraft'].max()):,}"
    )

with col4:
    st.metric(
        "Drone Losses",
        f"{int(df['drone'].max()):,}"
    )

# ==========================================
# DATASET PREVIEW
# ==========================================

st.subheader("Complete Dataset")
st.dataframe(df)

# ==========================================
# INDIVIDUAL METRIC ANALYSIS
# ==========================================

st.subheader(" Trend Analysis")

trend_metric = st.selectbox(
    "Select Category for Trend Analysis",
    metric_options,
    format_func=lambda x: friendly_names.get(x, x),
    key="trend"
)

fig, ax = plt.subplots(figsize=(12,6))

ax.plot(
    df["date"],
    df[trend_metric],
    linewidth=2
)

ax.set_title(
    f"{friendly_names[trend_metric]} Over Time"
)

ax.set_xlabel("Year")
ax.set_ylabel(
    friendly_names[trend_metric]
)

fig.autofmt_xdate()

st.pyplot(fig)

st.subheader("Multi-Category Trend Comparison")

selected_metrics = st.multiselect(
    "Select Categories",
    metric_options,
    default=["personnel", "tank"]
)

if selected_metrics:

    fig_multi, ax_multi = plt.subplots(figsize=(12,6))

    for metric in selected_metrics:
        ax_multi.plot(
            df["date"],
            df[metric],
            label=friendly_names[metric]
        )

    ax_multi.set_title(
        "Comparison of Loss Trends"
    )

    ax_multi.set_xlabel("Year")
    ax_multi.set_ylabel("Losses")

    ax_multi.legend()

    fig_multi.autofmt_xdate()

    st.pyplot(fig_multi)
# ==========================================
# COMPARISON DATA
# ==========================================

comparison_cols = [
    "tank",
    "aircraft",
    "helicopter",
    "apc",
    "field artillery",
    "drone"
]

latest = df[comparison_cols].iloc[-1]

# ==========================================
# EQUIPMENT COMPARISON
# ==========================================

with st.expander(" Equipment Loss Distribution"):

    fig3, ax3 = plt.subplots(figsize=(10,5))

    ax3.barh(
        [friendly_names[x] for x in comparison_cols],
        latest.values
    )

    ax3.set_title("Distribution of Equipment Losses")
    ax3.set_xlabel("Total Losses")
    ax3.set_ylabel("Equipment Category")

    st.pyplot(fig3)

# ==========================================
# LOSS DISTRIBUTION
# ==========================================

with st.expander(" Loss Distribution"):

    fig3, ax3 = plt.subplots(figsize=(8,8))

    wedges, texts = ax3.pie(
        latest.values,
        labels=None
    )

    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig3.gca().add_artist(centre_circle)

    ax3.legend(
        wedges,
        [friendly_names[x] for x in comparison_cols],
        title="Loss Categories",
        loc="center left",
        bbox_to_anchor=(1,0.5)
    )

    ax3.set_title("Distribution of Equipment Losses")

    st.pyplot(fig3)

# ==========================================
# CORRELATION MATRIX
# ==========================================

corr_cols = [
    "personnel",
    "tank",
    "aircraft",
    "helicopter",
    "apc",
    "field artillery",
    "mrl",
    "drone",
    "naval ship",
    "anti-aircraft warfare",
    "special equipment",
    "cruise missiles"
]

with st.expander(" Correlation Matrix"):

    corr_df = df[corr_cols].copy()

    corr_df.columns = [
        friendly_names[col]
        for col in corr_cols
    ]

    st.dataframe(
        corr_df.corr().round(2)
    )

# ==========================================
# TOP 10 PERSONNEL LOSS DAYS
# ==========================================

with st.expander(" Top 10 Highest Loss Records"):

    top_metric = st.selectbox(
        "Select Loss Category",
        corr_cols,
        format_func=lambda x: friendly_names.get(x, x),
        key="top10"
    )

    top10 = (
        df.nlargest(
            10,
            top_metric
        )[
            ["date", top_metric]
        ]
    )

    top10.columns = [
        "Date",
        friendly_names[top_metric]
    ]

    st.dataframe(top10)
# ==========================================
# SUMMARY STATISTICS
# ==========================================

with st.expander(" Summary Statistics"):

    summary_df = df[corr_cols].copy()

    summary_df.columns = [
        friendly_names[col]
        for col in corr_cols
    ]

    st.dataframe(
        summary_df.describe()
    )

# ==========================================
# LATEST VALUES TABLE
# ==========================================

with st.expander(" Latest Values Table"):

    latest_table = pd.DataFrame({
        "Loss Category": [
            friendly_names.get(col, col)
            for col in corr_cols
        ],
        "Latest Value": [
            df[col].max()
            for col in corr_cols
        ]
    })

    st.dataframe(latest_table)

# ==========================================
# KEY FINDINGS
# ==========================================

st.subheader(" Key Findings & Supporting Evidence")

# Finding 1
st.markdown("""
### 1. Personnel losses increased significantly over the duration of the conflict.
""")

with st.expander(" View Personnel Loss Trend"):

    fig, ax = plt.subplots(figsize=(10,5))

    ax.plot(df["date"], df["personnel"])

    ax.set_title("Personnel Losses Over Time")
    ax.set_xlabel("Year")
    ax.set_ylabel("Personnel Losses")

    st.pyplot(fig)

# Finding 2
st.markdown("""
### 2. Tank and Armored Vehicle losses exhibit strong positive correlation with personnel losses.
""")

with st.expander(" View Correlation Evidence"):

    corr_data = df[
        ["personnel","tank","apc"]
    ].corr().round(2)

    corr_data.columns = [
        "Personnel Losses",
        "Tank Losses",
        "Armored Vehicle Losses"
    ]

    corr_data.index = [
        "Personnel Losses",
        "Tank Losses",
        "Armored Vehicle Losses"
    ]

    st.dataframe(corr_data)

# Finding 3
st.markdown("""
### 3. Drone losses increased sharply, indicating growing reliance on drone warfare.
""")

with st.expander("View Drone Loss Trend"):

    fig, ax = plt.subplots(figsize=(10,5))

    ax.plot(df["date"], df["drone"])

    ax.set_title("Drone Losses Over Time")
    ax.set_xlabel("Year")
    ax.set_ylabel("Drone Losses")

    st.pyplot(fig)

# Finding 4
st.markdown("""
### 4. Ground equipment losses greatly exceed aircraft losses.
""")

with st.expander(" View Equipment Comparison"):

    compare = pd.DataFrame({
        "Category":[
            "Tank Losses",
            "Armored Vehicle Losses",
            "Aircraft Losses"
        ],
        "Losses":[
            df["tank"].max(),
            df["apc"].max(),
            df["aircraft"].max()
        ]
    })

    fig, ax = plt.subplots(figsize=(8, 4))

    ax.barh(
        compare["Category"],
        compare["Losses"]
    )

    st.pyplot(fig)

    st.dataframe(compare)

# Finding 5
st.markdown("""
### 5. Correlation analysis suggests that higher personnel losses often coincide with increased equipment losses.
""")

with st.expander(" View Full Correlation Matrix"):

    evidence_cols = [
        "personnel",
        "tank",
        "aircraft",
        "helicopter",
        "apc",
        "field artillery",
        "mrl",
        "drone",
        "naval ship",
        "anti-aircraft warfare",
        "special equipment",
        "cruise missiles"
    ]

    corr_matrix = df[evidence_cols].corr().round(2)

    st.dataframe(corr_matrix)

st.success("Dashboard Loaded Successfully ✅")
