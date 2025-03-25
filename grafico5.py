# Import data manipulation and visualization libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# === DATA INGESTION ===
# Load the GDP dataset from Statistics Canada
# This dataset contains quarterly estimates of gross domestic product (GDP) broken down by industrial sector
df = pd.read_csv(
    r"C:\Users\FabiodosSantosPrumuc\Desktop\meusdatasets\36100434.csv",
    encoding='latin1',
    low_memory=False
)

# Handle improperly encoded column name if present (common in CSVs from government sources)
if 'ï»¿REF_DATE' in df.columns:
    df.rename(columns={'ï»¿REF_DATE': 'REF_DATE'}, inplace=True)

# Clean column names by stripping trailing spaces
df.columns = df.columns.str.strip()

# Convert 'REF_DATE' from quarterly label to datetime format for time series analysis
df['REF_DATE'] = pd.PeriodIndex(df['REF_DATE'], freq='Q').to_timestamp()

# Remove rows with missing GDP values to ensure integrity of the analysis
df = df.dropna(subset=['VALUE'])

# === SECTOR SELECTION ===
# Exclude high-level aggregates (e.g., "All industries") to focus only on actual industrial sectors
excluded = [
    'All industries',
    'Goods-producing industries',
    'Service-producing industries',
    'Business sector industries'
]
df_industrial = df[~df['North American Industry Classification System (NAICS)'].isin(excluded)]

# Identify the top 5 industrial sectors with the highest cumulative GDP
top_5 = df_industrial.groupby(
    'North American Industry Classification System (NAICS)'
)['VALUE'].sum().nlargest(5).index.tolist()

# Filter dataset to include only the top 5 sectors
df_top5 = df_industrial[
    df_industrial['North American Industry Classification System (NAICS)'].isin(top_5)
]

# Group data by quarter and sector, summing GDP values for each combination
df_grouped = df_top5.groupby(
    ['REF_DATE', 'North American Industry Classification System (NAICS)']
)['VALUE'].sum().reset_index()

# === DATA VISUALIZATION ===
# Create a multi-line time series plot showing the quarterly GDP performance of the top 5 sectors

plt.figure(figsize=(14, 6))
sns.lineplot(
    data=df_grouped,
    x='REF_DATE',
    y='VALUE',
    hue='North American Industry Classification System (NAICS)'
)

# Add academic-quality formatting to the chart
plt.title('Quarterly GDP of Top 5 Industrial Sectors in Canada', fontsize=14)
plt.xlabel('Quarter')
plt.ylabel('GDP (in Millions, Chained 2017 Dollars)')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend(title='Industrial Sector')
plt.tight_layout()
plt.show()
