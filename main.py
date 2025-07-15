# gdp_co2_analysis.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 데이터 로드
df = pd.read_csv("data/gdp_co2_by_country.csv")

# 1. GDP vs CO₂ Emissions
def plot_gdp_vs_co2(country="United States"):
    data = df[df["Country Name"] == country]

    plt.figure(figsize=(10,6))
    sns.lineplot(x="Year", y="GDP USD", data=data, label="GDP (USD)")
    sns.lineplot(x="Year", y="CO2", data=data, label="CO₂ Emissions")
    plt.yscale("log")
    plt.title(f"{country}: GDP vs CO₂ Emissions (log scale)")
    plt.ylabel("Value (log-scaled)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"output/1_gdp_co2_{country.replace(' ', '_')}.png")
    plt.close()

# 2. Per Capita CO₂ Emissions (Top 10)
def plot_per_capita_top10(year=2020):
    df_year = df[df["Year"] == year].dropna(subset=["Per Capita CO2"])
    top10 = df_year.sort_values("Per Capita CO2", ascending=False).head(10)

    plt.figure(figsize=(10,6))
    sns.barplot(x="Per Capita CO2", y="Country Name", data=top10, palette="Reds_r")
    plt.title(f"Top 10 Countries by Per Capita CO₂ Emissions in {year}")
    plt.xlabel("CO₂ per Capita (metric tons)")
    plt.tight_layout()
    plt.savefig(f"output/2_top10_per_capita_{year}.png")
    plt.close()

# 3. CO₂ Emissions per GDP (Efficiency)
def plot_co2_efficiency(latest=True):
    year = df["Year"].max() if latest else 2020
    df_latest = df[df["Year"] == year]

    plt.figure(figsize=(8,6))
    sns.boxplot(x="GDP Category", y="CO2 Per GDP", data=df_latest)
    plt.title(f"CO₂ Emissions per GDP by GDP Category ({year})")
    plt.tight_layout()
    plt.savefig(f"output/3_co2_efficiency_{year}.png")
    plt.close()

# 4. GDP Growth vs CO₂ Change
def plot_growth_vs_emission(start_year=2000):
    df_recent = df[df["Year"] >= start_year].dropna(subset=["GDP %", "CO2 %"])

    plt.figure(figsize=(8,6))
    sns.scatterplot(x="GDP %", y="CO2 %", data=df_recent, alpha=0.4)
    sns.regplot(x="GDP %", y="CO2 %", data=df_recent, scatter=False, color="red")
    plt.title(f"GDP Growth vs CO₂ Emissions Change ({start_year}~)")
    plt.xlabel("GDP Growth Rate (%)")
    plt.ylabel("CO₂ Change Rate (%)")
    plt.tight_layout()
    plt.savefig(f"output/4_growth_vs_emission_{start_year}_plus.png")
    plt.close()

# 폴더 생성 (GitHub 웹에서는 수동 업로드 필요)
import os
os.makedirs("output", exist_ok=True)

# 실행
plot_gdp_vs_co2("United States")
plot_per_capita_top10(2020)
plot_co2_efficiency()
plot_growth_vs_emission()
