# Import core libraries for data handling and plotting
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# === DATA INGESTION ===
# Load monthly CPI data from the Bank of Canada dataset
# The dataset includes Total CPI and three core inflation measures used to assess underlying inflation trends
df = pd.read_csv(r"C:\Users\FabiodosSantosPrumuc\Desktop\meusdatasets\CPI_MONTHLY.csv")

# Convert the 'date' column to datetime format
df['date'] = pd.to_datetime(df['date'])

# Filter the dataset to include only observations from 1997 onwards
df = df[df['date'].dt.year >= 1997]

# Convert monthly data to quarterly periods
df['quarter'] = df['date'].dt.to_period('Q')

# === DATA AGGREGATION ===
# Group by quarter and compute the average of each inflation metric
# CPI core measures help identify trend inflation and filter out volatile components (like food or energy)
df_quarterly = df.groupby('quarter')[[
    'STATIC_TOTALCPICHANGE',  # Total CPI – headline inflation
    'CPI_TRIM',               # Trimmed CPI – excludes outlier price changes
    'CPI_MEDIAN',             # Median CPI – inflation at the midpoint
    'CPI_COMMON'              # Common CPI – shared component across categories
]].mean().reset_index()

# Convert 'quarter' back to timestamp for smoother plotting
df_quarterly['quarter'] = df_quarterly['quarter'].dt.to_timestamp()

# === DATA VISUALIZATION ===
# Generate a multi-line time series plot comparing all CPI inflation measures

plt.figure(figsize=(14, 6))

# Plot each CPI metric
sns.lineplot(data=df_quarterly, x='quarter', y='STATIC_TOTALCPICHANGE', label='Total CPI')
sns.lineplot(data=df_quarterly, x='quarter', y='CPI_TRIM', label='Trimmed CPI')
sns.lineplot(data=df_quarterly, x='quarter', y='CPI_MEDIAN', label='Median CPI')
sns.lineplot(data=df_quarterly, x='quarter', y='CPI_COMMON', label='Common CPI')

# Format x-axis to show only years
plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True, prune='both'))
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y'))

# Add academic chart elements
plt.title('Quarterly Inflation Trends in Canada (Averaged, from 1997)', fontsize=14)
plt.xlabel('Year')
plt.ylabel('Inflation Rate (%)')
plt.grid(True)
plt.legend(title="CPI Measure")
plt.tight_layout()

# Display the chart
plt.show()
