import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('../data/gdp_co2_by_country.csv')

usa = df[df['Country Name'] == 'United States']

plt.figure(figsize=(10,6))
sns.lineplot(x='Year', y='GDP USD', data=usa, label='GDP (USD)')
sns.lineplot(x='Year', y='CO2', data=usa, label='CO2 Emissions')

plt.title('GDP vs CO2 Emissions: United States')
plt.ylabel('Values (log-scale)')
plt.yscale('log')
plt.legend()
plt.tight_layout()
plt.show()

