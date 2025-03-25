# Importing essential libraries for data handling and visualization
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# === DATA INGESTION ===
# Load the Raw Materials Price Index (RMPI) dataset from Statistics Canada
# This dataset contains quarterly price indices for various raw materials used in the Canadian manufacturing sector.
df = pd.read_csv(
    r"C:\Users\FabiodosSantosPrumuc\Desktop\meusdatasets\18100268-RAW_QuarterNormal.csv",
    encoding='latin1',
    low_memory=False
)

# === DATA CLEANING ===
# Clean column names: remove trailing spaces and fix encoding artifacts (e.g., BOM markers)
df.columns = df.columns.str.strip().str.replace('\ufeff', '', regex=True)

# Convert the 'REF_DATE' column (in quarterly string format) into a proper datetime object
# This facilitates accurate time series visualization
df['REF_DATE'] = pd.PeriodIndex(df['REF_DATE'], freq='Q').to_timestamp()

# Remove rows where either the value or product classification is missing
df = df.dropna(subset=['VALUE', 'North American Product Classification System (NAPCS)'])

# === FEATURE SELECTION ===
# Identify the six most common raw material categories in the dataset based on frequency of appearance
# These are likely to represent the most impactful or widely used commodities
top_categories = df['North American Product Classification System (NAPCS)'].value_counts().head(6).index.tolist()

# Filter the dataset to retain only those top six categories
df_top = df[df['North American Product Classification System (NAPCS)'].isin(top_categories)]

# Group data by quarter and category, and calculate the mean price index
# This aggregation allows us to smooth out regional differences and focus on category-level trends
df_grouped = df_top.groupby(
    ['REF_DATE', 'North American Product Classification System (NAPCS)']
)['VALUE'].mean().reset_index()

# === DATA VISUALIZATION ===
# Plot a line chart to visualize the quarterly price index trends of the top raw material categories
# This helps identify inflation patterns, market volatility, and economic pressure points over time

plt.figure(figsize=(14, 6))
sns.lineplot(
    data=df_grouped,
    x='REF_DATE',
    y='VALUE',
    hue='North American Product Classification System (NAPCS)'
)

# Add academic-style titles and labels
plt.title('Graph 1 – RMPI Overview: Price Trends by Raw Material Category', fontsize=14)
plt.xlabel('Quarter')
plt.ylabel('Price Index (2020 = 100)')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend(title='Raw Material Category')
plt.tight_layout()
plt.show()

# Optional pause to allow chart inspection when running from command-line environments
input("✅ Pressione Enter to close the chart...")
