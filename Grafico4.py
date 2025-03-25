# Import libraries for data manipulation and visualization
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# === DATA INGESTION ===
# Load the Industrial Product Price Index (IPPI) dataset from Statistics Canada
# The dataset tracks price changes of manufactured goods sold by producers, covering various sectors
df = pd.read_csv(
    r"C:\Users\FabiodosSantosPrumuc\Desktop\meusdatasets\18100272-IPRI1203.csv",
    encoding='latin1',
    low_memory=False
)

# Handle BOM (byte order mark) if present in first column name
if 'ï»¿REF_DATE' in df.columns:
    df.rename(columns={'ï»¿REF_DATE': 'REF_DATE'}, inplace=True)

# Standardize column names by stripping extra spaces
df.columns = df.columns.str.strip()

# Convert 'REF_DATE' to datetime format using quarterly conversion
# This ensures compatibility with time series visualization
df['REF_DATE'] = pd.PeriodIndex(df['REF_DATE'], freq='Q').to_timestamp()

# Remove rows with missing key data (product name or value)
df = df.dropna(subset=['VALUE', 'North American Product Classification System (NAPCS)'])

# === VARIATION ANALYSIS ===
# Calculate price range (max - min) for each product across time
variation = df.groupby(
    'North American Product Classification System (NAPCS)'
)['VALUE'].agg(['max', 'min'])
variation['range'] = variation['max'] - variation['min']

# Identify top 5 products with highest price fluctuation (i.e., volatility)
top_products = variation.sort_values('range', ascending=False).head(5).index.tolist()

# Filter dataset to retain only the most volatile products
df_top = df[df['North American Product Classification System (NAPCS)'].isin(top_products)]

# Group data by time and product to compute the mean index value per quarter
df_grouped = df_top.groupby(
    ['REF_DATE', 'North American Product Classification System (NAPCS)']
)['VALUE'].mean().reset_index()

# === DATA VISUALIZATION ===
# Line plot showing how price indices evolved over time for the selected products

plt.figure(figsize=(14, 6))
sns.lineplot(
    data=df_grouped,
    x='REF_DATE',
    y='VALUE',
    hue='North American Product Classification System (NAPCS)'
)

# Format chart with academic-style title and axis labels
plt.title('IPPI Trends: Top 5 Industrial Products with Highest Price Variation', fontsize=14)
plt.xlabel('Quarter')
plt.ylabel('Price Index (2020=100)')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend(title='Industrial Product')
plt.tight_layout()
plt.show()

# Optional pause for CLI environments
input("✅ Pressione Enter para fechar o gráfico...")
