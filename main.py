import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# 설정: 시각화 스타일
sns.set(style="whitegrid")

def load_data(filepath: str) -> pd.DataFrame:
    """CSV 파일에서 데이터 불러오기"""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"파일이 존재하지 않습니다: {filepath}")
    return pd.read_csv(filepath)

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """최신 연도 데이터 필터링 및 전처리"""
    latest_year = df["Year"].max()
    df_latest = df[df["Year"] == latest_year].copy()

    # 필요한 열 존재 확인
    required_columns = ["GDP USD", "CO2", "Country Name", "Population", "GDP Category"]
    df_latest = df_latest.dropna(subset=required_columns)

    # 로그 변환
    df_latest["Log GDP"] = np.log10(df_latest["GDP USD"] + 1)
    df_latest["Log CO2"] = np.log10(df_latest["CO2"] + 1)

    return df_latest, latest_year

def plot_gdp_vs_co2(df: pd.DataFrame, year: int) -> None:
    """GDP vs CO2 산점도 시각화"""
    plt.figure(figsize=(10, 6))
    scatter = sns.scatterplot(
        data=df,
        x="Log GDP", y="Log CO2",
        hue="GDP Category", size="Population",
        sizes=(20, 300), palette="viridis", alpha=0.8, edgecolor="gray"
    )

    plt.title(f"GDP vs CO₂ Emissions (log scale) - {year}", fontsize=14)
    plt.xlabel("Log GDP (USD)")
    plt.ylabel("Log CO₂ Emissions (Metric Tons)")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
    plt.tight_layout()
    plt.savefig("gdp_vs_co2_plot.png")
    plt.show()

def main():
    data_path = "gdp_co2_by_country.csv"

    try:
        df = load_data(data_path)
        df_processed, year = preprocess_data(df)
        plot_gdp_vs_co2(df_processed, year)
        print(f"분석 완료: {year}년 데이터 시각화 완료 (파일 저장됨: gdp_vs_co2_plot.png)")
    except Exception as e:
        print(f"[오류 발생] {e}")

if __name__ == "__main__":
    main()
