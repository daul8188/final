import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# 페이지 기본 설정
st.set_page_config(page_title="GDP vs CO₂ Emissions", layout="wide")
st.title("🌍 GDP vs CO₂ Emissions Dashboard")
st.markdown("시각화를 통해 세계 각국의 경제와 환경 사이의 관계를 살펴보세요.")

# 데이터 로드 함수
@st.cache_data
def load_data():
    df = pd.read_csv("gdp_co2_by_country.csv")
    df = df.dropna(subset=["GDP USD", "CO2", "Country Name", "Year", "Population", "GDP Category"])
    return df

# 데이터 불러오기
df = load_data()

# 연도 선택
years = sorted(df["Year"].unique(), reverse=True)
selected_year = st.selectbox("📅 연도 선택", years)

# 해당 연도 데이터 필터링
df_year = df[df["Year"] == selected_year].copy()
df_year["Log GDP"] = np.log10(df_year["GDP USD"] + 1)
df_year["Log CO2"] = np.log10(df_year["CO2"] + 1)

# 그래프 출력
st.subheader(f"📈 GDP vs CO₂ Emissions (log scale) - {selected_year}")

fig, ax = plt.subplots(figsize=(10, 6))
scatter = sns.scatterplot(
    data=df_year,
    x="Log GDP", y="Log CO2",
    hue="GDP Category", size="Population",
    palette="viridis", sizes=(30, 300), alpha=0.7, edgecolor="gray", legend=False
)
ax.set_xlabel("Log GDP (USD)")
ax.set_ylabel("Log CO₂ Emissions (Metric Tons)")
st.pyplot(fig)

# 데이터 미리보기
with st.expander("🔍 데이터 테이블 보기"):
    st.dataframe(df_year[["Country Name", "GDP USD", "CO2", "Population", "GDP Category"]].sort_values(by="GDP USD", ascending=False))
