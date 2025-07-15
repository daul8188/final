# streamlit_app.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="GDP & CO₂ Dashboard", layout="wide")

st.title("🌍 Global GDP & CO₂ Emissions Analysis")

# 파일 경로
DATA_PATH = "data/gdp_co2_by_country.csv"

# 데이터 불러오기 (Streamlit Cloud에서 에러 방지용 처리 포함)
@st.cache_data
def load_data():
    if not os.path.exists(DATA_PATH):
        return None
    return pd.read_csv(DATA_PATH)

df = load_data()

if df is None:
    st.warning(f"""
    ❗ 데이터 파일이 존재하지 않습니다.

    📌 아래 조건을 확인하세요:
    - `data/gdp_co2_by_country.csv` 파일을 GitHub 저장소에 업로드했나요?
    - `streamlit_app.py`와 같은 저장소에 있고, `data/` 폴더 안에 있어야 합니다.
    
    예:  
    ├── data/  
    │   └── gdp_co2_by_country.csv  
    └── streamlit_app.py
    """)
    st.stop()

# 사이드바 설정
st.sidebar.header("🔧 분석 설정")
country = st.sidebar.selectbox("국가 선택", sorted(df["Country Name"].unique()), index=0)
year = st.sidebar.slider("연도 선택 (Per Capita 분석)", min_value=int(df["Year"].min()), max_value=int(df["Year"].max()), value=2020)
start_year = st.sidebar.slider("시작 연도 (성장률 vs 배출)", min_value=1960, max_value=2022, value=2000)

# 1. GDP vs CO₂
st.subheader("1. GDP vs CO₂ Emissions")
df_country = df[df["Country Name"] == country]
fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.lineplot(data=df_country, x="Year", y="GDP USD", label="GDP", ax=ax1)
sns.lineplot(data=df_country, x="Year", y="CO2", label="CO₂ Emissions", ax=ax1)
ax1.set_yscale("log")
ax1.set_title(f"{country}: GDP vs CO₂ Emissions (log scale)")
st.pyplot(fig1)

# 2. Per Capita CO₂ Top 10
st.subheader("2. Per Capita CO₂ Emissions Top 10")
df_year = df[df["Year"] == year].dropna(subset=["Per Capita CO2"])
top10 = df_year.sort_values("Per Capita CO2", ascending=False).head(10)
fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.barplot(data=top10, x="Per Capita CO2", y="Country Name", palette="Reds_r", ax=ax2)
ax2.set_title(f"Top 10 CO₂ Emitters per Capita ({year})")
st.pyplot(fig2)

# 3. CO₂ 효율성 (GDP 대비 배출량)
st.subheader("3. CO₂ Emission Efficiency by GDP Category")
df_eff = df[df["Year"] == year]
fig3, ax3 = plt.subplots(figsize=(8, 5))
sns.boxplot(data=df_eff, x="GDP Category", y="CO2 Per GDP", ax=ax3)
ax3.set_title(f"CO₂ per GDP by Category ({year})")
st.pyplot(fig3)

# 4. GDP 성장률 vs CO₂ 배출 변화율
st.subheader("4. GDP Growth Rate vs CO₂ Emissions Change")
df_growth = df[df["Year"] >= start_year].dropna(subset=["GDP %", "CO2 %"])
fig4, ax4 = plt.subplots(figsize=(8, 5))
sns.scatterplot(data=df_growth, x="GDP %", y="CO2 %", alpha=0.4, ax=ax4)
sns.regplot(data=df_growth, x="GDP %", y="CO2 %", scatter=False, color="red", ax=ax4)
ax4.set_title(f"GDP Growth vs CO₂ Change (from {start_year})")
st.pyplot(fig4)
