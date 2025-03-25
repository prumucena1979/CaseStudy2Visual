# Import core libraries for data manipulation and visualization
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# === DATA INGESTION ===
# Load the Raw Materials Price Index (RMPI) dataset from Statistics Canada
# The dataset includes quarterly price indices for a variety of raw materials critical to the Canadian economy
df = pd.read_csv(
    r"C:\Users\FabiodosSantosPrumuc\Desktop\meusdatasets\18100268-RAW_QuarterNormal.csv",
    encoding='latin1',
    low_memory=False
)

# === DATA CLEANING ===
# Standardize column names and remove potential byte order marks (BOM)
df.columns = df.columns.str.strip().str.replace('\ufeff', '', regex=True)

# Convert reference date column to datetime object for time series plotting
df['REF_DATE'] = pd.PeriodIndex(df['REF_DATE'], freq='Q').to_timestamp()

# Drop entries with missing values in key analytical columns
df = df.dropna(subset=['VALUE', 'North American Product Classification System (NAPCS)'])

# === VARIATION ANALYSIS ===
# Group data by product category and calculate minimum and maximum price index values
# Then compute the range (i.e., price variation) for each product
variation = df.groupby(
    'North American Product Classification System (NAPCS)'
)['VALUE'].agg(['min', 'max'])
variation['range'] = variation['max'] - variation['min']

# Identify the top 5 products with the highest price variation
top_products = variation.sort_values('range', ascending=False).head(5).index.tolist()

# Filter the main dataset to include only those top 5 volatile products
df_top = df[df['North American Product Classification System (NAPCS)'].isin(top_products)]

# Group filtered data by time and product category to compute mean price index per quarter
df_grouped = df_top.groupby(
    ['REF_DATE', 'North American Product Classification System (NAPCS)']
)['VALUE'].mean().reset_index()

# === DATA VISUALIZATION ===
# Line plot to visualize the quarterly price evolution of the most volatile raw materials
# Helps identify which materials are most prone to economic pressure

plt.figure(figsize=(14, 6))
sns.lineplot(
    data=df_grouped,
    x='REF_DATE',
    y='VALUE',
    hue='North American Product Classification System (NAPCS)'
)

# Chart formatting for academic presentation
plt.title('Graph 2 – RMPI: Top 5 Raw Materials with Highest Price Variation', fontsize=14)
plt.xlabel('Quarter')
plt.ylabel('Price Index (2020 = 100)')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend(title='Raw Material')
plt.tight_layout()
plt.show()

# Pause to allow chart inspection when run in command-line interface
input("✅ Pressione Enter to close the chart...")
