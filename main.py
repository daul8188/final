import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('../data/gdp_co2_by_country.csv')

# 2020년 이후 데이터 (변화율 관찰)
df_recent = df[df['Year'] >= 2000].dropna(subset=['CO2 %', 'GDP %'])

plt.figure(figsize=(8,6))
sns.scatterplot(x='GDP %', y='CO2 %', data=df_recent, alpha=0.5)
sns.regplot(x='GDP %', y='CO2 %', data=df_recent, scatter=False, color='red')

plt.title('GDP Growth vs CO₂ Emissions Change (2000~)')
plt.xlabel('GDP Growth Rate (%)')
plt.ylabel('CO₂ Emissions Change Rate (%)')
plt.tight_layout()
plt.show()
