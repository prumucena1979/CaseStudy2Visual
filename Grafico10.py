import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load and preprocess
df = pd.read_csv(r"C:\Users\FabiodosSantosPrumuc\Desktop\meusdatasets\Datasets\CPI_MONTHLY.csv")
df['date'] = pd.to_datetime(df['date'])
df = df[df['date'].dt.year >= 1997]
df['quarter'] = df['date'].dt.to_period('Q')
df_quarterly = df.groupby('quarter')[['STATIC_TOTALCPICHANGE', 'CPI_TRIM', 'CPI_MEDIAN', 'CPI_COMMON']].mean().reset_index()
df_quarterly['quarter'] = df_quarterly['quarter'].dt.to_timestamp()

# Plot
plt.figure(figsize=(14, 6))
sns.lineplot(data=df_quarterly, x='quarter', y='STATIC_TOTALCPICHANGE', label='Total CPI')
sns.lineplot(data=df_quarterly, x='quarter', y='CPI_TRIM', label='Trimmed CPI')
sns.lineplot(data=df_quarterly, x='quarter', y='CPI_MEDIAN', label='Median CPI')
sns.lineplot(data=df_quarterly, x='quarter', y='CPI_COMMON', label='Common CPI')

# Highlight crises
plt.axvspan(pd.to_datetime('2008-07-01'), pd.to_datetime('2010-12-31'), color='red', alpha=0.1, label='2008–2009 Crisis')
plt.axvspan(pd.to_datetime('2020-01-01'), pd.to_datetime('2021-12-31'), color='orange', alpha=0.1, label='COVID-19 Crisis')

# Formatting
plt.title('Inflation Trends During Global Crises (Canada)', fontsize=14)
plt.xlabel('Year')
plt.ylabel('Inflation Rate (%)')
plt.grid(True)
plt.legend(title='CPI Measure', loc='upper left')
plt.tight_layout()
plt.show()
