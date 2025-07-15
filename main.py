import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 출력 디렉토리 생성
os.makedirs("output/data", exist_ok=True)
os.makedirs("output/figures", exist_ok=True)

# 데이터 불러오기
df = pd.read_csv("data/gdp_co2_by_country.csv")

# 1. 국가별 GDP vs CO₂ Emissions
def gdp_vs_co2(country="United States"):
    data = df[df["Country Name"] == country]
    filename = country.replace(" ", "_")

    # 데이터 저장
    data.to_csv(f"output/data/1_gdp_co2_{filename}.csv", index=False)

    # 그래프
    plt.figure(figsize=(10,6))
    sns.lineplot(x="Year", y="GDP USD", data=data, label="GDP (USD)")
    sns.lineplot(x="Year", y="CO2", data=data, label="CO₂ Emissions")
    plt.yscale("log")
    plt.title(f"{country}: GDP vs CO₂ Emissions (log scale)")
    plt.xlabel("Year")
    plt.ylabel("Log-scaled Value")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"output/figures/1_gdp_co2_{filename}.png")
    plt.close()


# 2. 특정 연도: 1인당 CO₂ 배출 상위 10개국
def per_capita_top10(year=2020):
    data = df[df["Year"] == year].dropna(subset=["Per Capita CO2"])
    top10 = data.sort_values("Per Capita CO2", ascending=False).head(10)

    # 데이터 저장
    top10.to_csv(f"output/data/2_top10_per_capita_{year}.csv", index=False)

    # 그래프
    plt.figure(figsize=(10,6))
    sns.barplot(x="Per Capita CO2", y="Country Name", data=top10, palette="Reds_r")
    plt.title(f"Top 10 Countries by Per Capita CO₂ Emissions ({year})")
    plt.xlabel("CO₂ per Capita (metric tons)")
    plt.tight_layout()
    plt.savefig(f"output/figures/2_top10_per_capita_{year}.png")
    plt.close()


# 3. CO₂ 배출 효율성 (CO₂ per GDP): 특정 연도
def co2_efficiency_by_gdp(year=None):
    if year is None:
        year = df["Year"].max()
    data = df[df["Year"] == year]

    # 데이터 저장
    data.to_csv(f"output/data/3_co2_efficiency_{year}.csv", index=False)

    # 그래프
    plt.figure(figsize=(8,6))
    sns.boxplot(x="GDP Category", y="CO2 Per GDP", data=data)
    plt.title(f"CO₂ Emissions per GDP by GDP Category ({year})")
    plt.tight_layout()
    plt.savefig(f"output/figures/3_co2_efficiency_{year}.png")
    plt.close()


# 4. GDP 성장률 vs CO₂ 변화율 (산점도): 시작 연도부터
def growth_vs_emission(start_year=2000):
    data = df[df["Year"] >= start_year].dropna(subset=["GDP %", "CO2 %"])

    # 데이터 저장
    data.to_csv(f"output/data/4_growth_vs_emission_from_{start_year}.csv", index=False)

    # 그래프
    plt.figure(figsize=(8,6))
    sns.scatterplot(x="GDP %", y="CO2 %", data=data, alpha=0.4)
    sns.regplot(x="GDP %", y="CO2 %", data=data, scatter=False, color="red")
    plt.title(f"GDP Growth vs CO₂ Emissions Change (from {start_year})")
    plt.xlabel("GDP Growth Rate (%)")
    plt.ylabel("CO₂ Change Rate (%)")
    plt.tight_layout()
    plt.savefig(f"output/figures/4_growth_vs_emission_from_{start_year}.png")
    plt.close()

# ------------------------------
# 💡 아래에서 직접 분석 항목 실행!
# 원하는 값으로 함수 호출만 하면 됨
# ------------------------------

# 예시 실행 (필요한 것만 골라서 실행 가능)
gdp_vs_co2("South Korea")
per_capita_top10(2021)
co2_efficiency_by_gdp(2020)
growth_vs_emission(2005)
