# streamlit_app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(page_title="GDP & CO₂ Analysis", layout="wide")
st.title("🌍 Global GDP & CO₂ Emissions Analysis")

# ✅ CSV 파일이 같은 폴더에 있다고 가정
CSV_FILENAME = "gdp_co2_by_country.csv"

# 데이터 로드 함수
@st.cache_data
def load_data():
    if not os.path.exists(CSV_FILENAME):
        return None
    return pd.read_csv(CSV_FILENAME)

df = load_data()

# 데이터가 없으면 사용자에게 경고
if df is None:
    st.error(f"""
    ❗ '{CSV_FILENAME}' 파일이 현재 이 파일(streamlit_app.py)과 같은 위치에 없습니다.

    👉 해결 방법:
    - GitHub 저장소에 `streamlit_app.py` 파일과 함께
    - `gdp_co2_by_country.csv` 파일도 같은 폴더에 업로드하세요.

    예:
    ├── streamlit_app.py  
    └── gdp_co2_by_country.csv  
    """)
    st.stop()

# 사이드바
st.sidebar.header("🔧 분석 설정")
country = st.sidebar.selectbox("국가 선택", sorted(df["Country Name"].unique()))
year = st.sidebar.slider("연도 선택 (Per Capita 분석)", int(df["Year"].min()), int(df["Year"].max()), 2020)
start_year = st.sidebar.slider("시작 연도 (GDP vs CO2 변화)", 1960, 2022, 2000)

# 1. GDP vs CO₂
st.subheader("1. GDP vs CO₂ Emissions")
df_country = df[df["Country Name"] == country]
fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.lineplot(data=df_country, x="Year", y="GDP USD", label="GDP", ax=ax1)
sns.lineplot(data=df_country, x="Year", y="CO2", label="CO₂ Emissions", ax=ax1)
ax1.set_yscale("log")
ax1.set_title(f"{country}: GDP vs CO₂ Emissions")
st.pyplot(fig1)

# 2. Per Capita CO₂ Top 10
st.subheader("2. Top 10 Per Capita CO₂ Emitters")
df_year = df[df["Year"] == year].dropna(subset=["Per Capita CO2"])
top10 = df_year.sort_values("Per Capita CO2", ascending=False).head(10)
fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.barplot(data=top10, x="Per Capita CO2", y="Country Name", palette="Reds_r", ax=ax2)
ax2.set_title(f"Top 10 CO₂ per Capita ({year})")
st.pyplot(fig2)

# 3. CO₂ per GDP (Efficiency)
st.subheader("3. CO₂ Emissions per GDP (Efficiency)")
df_eff = df[df["Year"] == year]
fig3, ax3 = plt.subplots(figsize=(8, 5))
sns.boxplot(data=df_eff, x="GDP Category", y="CO2 Per GDP", ax=ax3)
ax3.set_title(f"CO₂ Efficiency by GDP Category ({year})")
st.pyplot(fig3)

# 4. GDP Growth vs CO₂ Change
st.subheader("4. GDP Growth vs CO₂ Change")
df_growth = df[df["Year"] >= start_year].dropna(subset=["GDP %", "CO2 %"])
fig4, ax4 = plt.subplots(figsize=(8, 5))
sns.scatterplot(data=df_growth, x="GDP %", y="CO2 %", alpha=0.4, ax=ax4)
sns.regplot(data=df_growth, x="GDP %", y="CO2 %", scatter=False, color="red", ax=ax4)
ax4.set_title(f"GDP Growth vs CO₂ Change Rate (from {start_year})")
st.pyplot(fig4)
