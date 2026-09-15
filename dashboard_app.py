import os
import glob
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as gg
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Appendix Cancer Prediction Dashboard",
    page_icon="🏥",
    layout="wide"
)

# Custom Styling
st.markdown("""
<style>
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .metric-title {
        font-size: 13px;
        color: #64748B;
        font-weight: 600;
        text-transform: uppercase;
    }
    .metric-value {
        font-size: 26px;
        color: #0F172A;
        font-weight: 700;
        margin-top: 4px;
    }
</style>
""", unsafe_allow_html=True)

# Data Loader
@st.cache_data
def load_data():
    csv_file = "appendix_cancer_analyzed.csv"
    if not os.path.exists(csv_file):
        import subprocess
        subprocess.run(["python3", "run_analysis.py"], check=True)
    
    df = pd.read_csv(csv_file)
    return df

df = load_data()

# Header
st.title("🏥 Appendix Cancer Prediction & Clinical Analytics Dashboard")
st.markdown("Interactive clinical analytical dashboard exploring 260,000 patient records and 63 calculated metrics.")
st.divider()

# Sidebar Filters
st.sidebar.header("🔍 Dashboard Filters")

# Country Filter
all_countries = ["All"] + sorted(list(df["Country"].dropna().unique()))
selected_country = st.sidebar.selectbox("Select Country", all_countries)

# Gender Filter
all_genders = ["All"] + sorted(list(df["Gender"].dropna().unique()))
selected_gender = st.sidebar.selectbox("Select Gender", all_genders)

# Age Group Filter
if "IF_Age_Group" in df.columns:
    age_groups = ["All"] + sorted(list(df["IF_Age_Group"].dropna().unique()))
else:
    age_groups = ["All", "Senior", "Adult", "Youth"]
selected_age_group = st.sidebar.selectbox("Select Age Group", age_groups)

# Risk Category Filter
if "IIF_High_Risk" in df.columns:
    risk_categories = ["All"] + sorted(list(df["IIF_High_Risk"].dropna().unique()))
else:
    risk_categories = ["All", "High Risk", "Standard Risk"]
selected_risk = st.sidebar.selectbox("Select Risk Profile", risk_categories)

# Apply Filtering
filtered_df = df.copy()

if selected_country != "All":
    filtered_df = filtered_df[filtered_df["Country"] == selected_country]

if selected_gender != "All":
    filtered_df = filtered_df[filtered_df["Gender"] == selected_gender]

if selected_age_group != "All" and "IF_Age_Group" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["IF_Age_Group"] == selected_age_group]

if selected_risk != "All" and "IIF_High_Risk" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["IIF_High_Risk"] == selected_risk]

# KPI Summary Row
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

total_patients = len(filtered_df)
cancer_pos_count = (filtered_df["Appendix_Cancer_Prediction"] == "Yes").sum()
cancer_pos_rate = (cancer_pos_count / total_patients * 100) if total_patients > 0 else 0.0
avg_survival = filtered_df["Survival_Years_After_Diagnosis"].mean() if total_patients > 0 else 0.0
avg_delay = filtered_df["Diagnosis_Delay_Days"].mean() if total_patients > 0 else 0.0

with kpi1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Total Patients</div>
        <div class="metric-value">{total_patients:,}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Cancer Positive Rate</div>
        <div class="metric-value">{cancer_pos_rate:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Avg Survival Years</div>
        <div class="metric-value">{avg_survival:.1f} yrs</div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Avg Diagnosis Delay</div>
        <div class="metric-value">{avg_delay:.0f} days</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Row 1: Map + Demographics
col_map, col_demo = st.columns([1.2, 1])

with col_map:
    st.subheader("🌍 Geographic Patient Distribution & Cancer Rates")
    country_summary = filtered_df.groupby("Country").agg(
        Total_Patients=("Patient_ID", "count"),
        Cancer_Positive=("Appendix_Cancer_Prediction", lambda x: (x == "Yes").sum())
    ).reset_index()
    country_summary["Cancer_Rate_%"] = (country_summary["Cancer_Positive"] / country_summary["Total_Patients"] * 100).round(1)
    
    fig_map = px.choropleth(
        country_summary,
        locations="Country",
        locationmode="country names",
        color="Total_Patients",
        hover_name="Country",
        hover_data={"Total_Patients": ":,", "Cancer_Rate_%": ":.1f%"},
        color_continuous_scale="Viridis",
        labels={"Total_Patients": "Patients"}
    )
    fig_map.update_layout(margin=dict(l=0, r=0, t=20, b=0), height=380)
    st.plotly_chart(fig_map, use_container_width=True)

with col_demo:
    st.subheader("📊 Cancer Prediction by Age Group & Gender")
    if "IF_Age_Group" in filtered_df.columns:
        demo_df = filtered_df.groupby(["IF_Age_Group", "Gender", "Appendix_Cancer_Prediction"]).size().reset_index(name="Count")
        fig_demo = px.bar(
            demo_df,
            x="IF_Age_Group",
            y="Count",
            color="Appendix_Cancer_Prediction",
            barmode="group",
            facet_col="Gender",
            color_discrete_map={"Yes": "#EF4444", "No": "#10B981"},
            labels={"IF_Age_Group": "Age Group", "Appendix_Cancer_Prediction": "Cancer Positive?"}
        )
        fig_demo.update_layout(height=380, margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig_demo, use_container_width=True)

st.divider()

# Row 2: Biomarkers + Treatment
col_bio, col_treat = st.columns(2)

with col_bio:
    st.subheader("🧬 Clinical Biomarkers Comparison")
    bio_summary = filtered_df.groupby("Appendix_Cancer_Prediction").agg(
        Avg_BMI=("BMI", "mean"),
        Avg_Cholesterol=("Cholesterol_Level", "mean"),
        Avg_Blood_Pressure=("Blood_Pressure", "mean")
    ).reset_index()
    
    fig_bio = gg.Figure()
    fig_bio.add_trace(gg.Bar(x=bio_summary["Appendix_Cancer_Prediction"], y=bio_summary["Avg_BMI"], name="Avg BMI"))
    fig_bio.add_trace(gg.Bar(x=bio_summary["Appendix_Cancer_Prediction"], y=bio_summary["Avg_Cholesterol"], name="Avg Cholesterol"))
    fig_bio.add_trace(gg.Bar(x=bio_summary["Appendix_Cancer_Prediction"], y=bio_summary["Avg_Blood_Pressure"], name="Avg Blood Pressure"))
    fig_bio.update_layout(barmode="group", height=350, margin=dict(l=0, r=0, t=30, b=0), xaxis_title="Cancer Prediction Status")
    st.plotly_chart(fig_bio, use_container_width=True)

with col_treat:
    st.subheader("🏥 Treatment Type vs Survival Rate")
    treat_summary = filtered_df.groupby("Treatment_Type")["Survival_Years_After_Diagnosis"].mean().reset_index()
    treat_summary.columns = ["Treatment_Type", "Avg_Survival_Years"]
    treat_summary = treat_summary.sort_values("Avg_Survival_Years", ascending=True)
    
    fig_treat = px.bar(
        treat_summary,
        x="Avg_Survival_Years",
        y="Treatment_Type",
        orientation="h",
        color="Avg_Survival_Years",
        color_continuous_scale="Tealgrn",
        labels={"Avg_Survival_Years": "Avg Survival (Years)", "Treatment_Type": "Treatment Type"}
    )
    fig_treat.update_layout(height=350, margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig_treat, use_container_width=True)

st.divider()

# Row 3: Raw Data Preview
st.subheader("📋 Filtered Patient Dataset Records")
preview_cols = [c for c in ["Patient_ID", "Country", "Age", "Gender", "BMI", "Blood_Pressure", "Symptom_Severity", "Treatment_Type", "Appendix_Cancer_Prediction", "IF_Age_Group", "IIF_High_Risk"] if c in filtered_df.columns]
st.dataframe(filtered_df[preview_cols].head(100), use_container_width=True)
