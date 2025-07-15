# 분석: GDP와 CO2 배출량의 관계 (기초 시각화)
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1. 데이터 로드
df = pd.read_csv("gdp_co2_by_country.csv")

# 2. 최근 연도 데이터만 사용 (예: 2020)
latest_year = df["Year"].max()
df_latest = df[df["Year"] == latest_year].copy()

# 3. 결측치 제거
df_latest = df_latest.dropna(subset=["GDP USD", "CO2", "Country Name"])

# 4. 로그 변환 (시각화용)
df_latest["Log GDP"] = np.log10(df_latest["GDP USD"] + 1)
df_latest["Log CO2"] = np.log10(df_latest["CO2"] + 1)

# 5. 산점도 시각화 (GDP vs CO2)
plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=df_latest,
    x="Log GDP", y="Log CO2",
    hue="GDP Category", size="Population",
    alpha=0.7, palette="viridis", sizes=(20, 200)
)
plt.title(f"GDP vs CO₂ Emissions (log scale) - {latest_year}")
plt.xlabel("Log GDP (USD)")
plt.ylabel("Log CO₂ Emissions (Metric Tons)")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()
