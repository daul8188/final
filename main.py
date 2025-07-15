import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 폴더 생성
os.makedirs("output/data", exist_ok=True)
os.makedirs("output/figures", exist_ok=True)

# CSV 파일 경로 (수정 가능)
DATA_PATH = "data/gdp_co2_by_country.csv"

# 데이터 불러오기
try:
    df = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    raise FileNotFoundError(f"CSV 파일이 '{DATA_PATH}' 경로에 없습니다. GitHub에 업로드했는지 확인하세요.")

# 1. 국가별 GDP vs CO₂
def analyze_gdp_vs_co2(country):
    country_df = df[df["Country Name"] == country]
    filename = country.replace(" ", "_")

    if country_df.empty:
        print(f"[경고] '{country}'에 해당하는 데이터가 없습니다.")
        return

    country_df.to_csv(f"output/data/1_gdp_co2_{filename}.csv", index=False)

    plt.figure(figsize=(10,6))
    sns.lineplot(x="Year", y="GDP USD", data=country_df, label="GDP (USD)")
    sns.lineplot(x="Year", y="CO2", data=country_df, label="CO₂ Emissions")
    plt.yscale("log")
    plt.title(f"{country}: GDP vs CO₂ Emissions")
    plt.xlabel("Year")
    plt.ylabel("Log-scaled Value")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"output/figures/1_gdp_co2_{filename}.png")
    plt.close()
    print(f"[완료] 1. GDP vs CO₂ 분석 저장됨 → {filename}")

# 2. 1인당 CO₂ 상위 10개국
def analyze_per_capita_top10(year):
    year_df = df[df["Year"] == year].dropna(subset=["Per Capita CO2"])
    if year_df.empty:
        print(f"[경고] {year}년 데이터가 없습니다.")
        return

    top10 = year_df.sort_values("Per Capita CO2", ascending=False).head(10)
    top10.to_csv(f"output/data/2_top10_per_capita_{year}.csv", index=False)

    plt.figure(figsize=(10,6))
    sns.barplot(x="Per Capita CO2", y="Country Name", data=top10, palette="Reds_r")
    plt.title(f"Top 10 Countries by Per Capita CO₂ Emissions in {year}")
    plt.xlabel("CO₂ per Capita (metric tons)")
    plt.tight_layout()
    plt.savefig(f"output/figures/2_top10_per_capita_{year}.png")
    plt.close()
    print(f"[완료] 2. Per Capita Top 10 저장됨 → {year}")

# 3. CO₂ per GDP (효율성)
def analyze_efficiency(year):
    year_df = df[df["Year"] == year]
    if year_df.empty:
        print(f"[경고] {year}년 데이터가 없습니다.")
        return

    year_df.to_csv(f"output/data/3_co2_efficiency_{year}.csv", index=False)

    plt.figure(figsize=(8,6))
    sns.boxplot(x="GDP Category", y="CO2 Per GDP", data=year_df)
    plt.title(f"CO₂ Emissions per GDP by Category ({year})")
    plt.tight_layout()
    plt.savefig(f"output/figures/3_co2_efficiency_{year}.png")
    plt.close()
    print(f"[완료] 3. CO₂ 효율성 저장됨 → {year}")

# 4. 성장률 vs CO₂ 변화율
def analyze_growth_vs_emission(start_year):
    filtered = df[df["Year"] >= start_year].dropna(subset=["GDP %", "CO2 %"])
    if filtered.empty:
        print(f"[경고] {start_year}년 이후 데이터가 없습니다.")
        return

    filtered.to_csv(f"output/data/4_growth_vs_emission_from_{start_year}.csv", index=False)

    plt.figure(figsize=(8,6))
    sns.scatterplot(x="GDP %", y="CO2 %", data=filtered, alpha=0.5)
    sns.regplot(x="GDP %", y="CO2 %", data=filtered, scatter=False, color="red")
    plt.title(f"GDP Growth vs CO₂ Emissions Change (from {start_year})")
    plt.xlabel("GDP Growth Rate (%)")
    plt.ylabel("CO₂ Change Rate (%)")
    plt.tight_layout()
    plt.savefig(f"output/figures/4_growth_vs_emission_from_{start_year}.png")
    plt.close()
    print(f"[완료] 4. 성장률 vs 배출량 변화 저장됨 → {start_year}~")

# ========================
# ✅ 여기서 설정하면 됨
# ========================

# 분석 파라미터 직접 지정!
analyze_gdp_vs_co2("South Korea")
analyze_per_capita_top10(2020)
analyze_efficiency(2021)
analyze_growth_vs_emission(2005)
