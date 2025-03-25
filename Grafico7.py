# Import libraries for data handling and time series visualization
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# === DATA INGESTION ===
# Load the quarterly GDP dataset from Statistics Canada
# The dataset contains GDP values by industry sector, adjusted for inflation (chained 2017 dollars)
df = pd.read_csv(
    r"C:\Users\FabiodosSantosPrumuc\Desktop\meusdatasets\36100434.csv",
    encoding='latin1',
    low_memory=False
)

# Handle broken column name if present (caused by encoding artifacts)
if 'ï»¿REF_DATE' in df.columns:
    df.rename(columns={'ï»¿REF_DATE': 'REF_DATE'}, inplace=True)

# Convert quarterly string values (e.g., '1997Q1') into timestamp format for plotting
df['REF_DATE'] = pd.PeriodIndex(df['REF_DATE'], freq='Q').to_timestamp()

# Remove rows where the GDP value is missing
df = df.dropna(subset=['VALUE'])

# === SECTOR RANKING ===
# Group by sector and calculate total GDP contribution over time
# Identify the top 3 industry sectors based on cumulative economic output
top_sectors = df.groupby('North American Industry Classification System (NAICS)')['VALUE'].sum().nlargest(3).index.tolist()

# Filter dataset to retain only those top 3 sectors
df_top = df[df['North American Industry Classification System (NAICS)'].isin(top_sectors)]

# Aggregate quarterly GDP values per sector
df_grouped = df_top.groupby(
    ['REF_DATE', 'North American Industry Classification System (NAICS)']
)['VALUE'].sum().reset_index()

# === DATA VISUALIZATION ===
# Generate a multi-line plot to visualize the GDP trends of the top 3 sectors

plt.figure(figsize=(14, 6))
sns.lineplot(
    data=df_grouped,
    x='REF_DATE',
    y='VALUE',
    hue='North American Industry Classification System (NAICS)'
)

# Academic-style formatting for interpretability
plt.title('Quarterly GDP of Top 3 Industry Sectors in Canada', fontsize=14)
plt.xlabel('Quarter')
plt.ylabel('GDP (in Millions, Chained 2017 Dollars)')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend(title='Industry Sector')
plt.tight_layout()
plt.show()
