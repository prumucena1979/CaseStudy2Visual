# Import core libraries for data handling and plotting
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# === DATA INGESTION ===
# Load the Raw Materials Price Index (RMPI) dataset
# This dataset contains historical quarterly indices for various raw materials used in Canadian industry
df = pd.read_csv(
    r"C:\Users\FabiodosSantosPrumuc\Desktop\meusdatasets\18100268-RAW_QuarterNormal.csv",
    encoding='latin1',
    low_memory=False
)

# === DATA CLEANING ===
# Remove unwanted characters and ensure column names are properly formatted
df.columns = df.columns.str.strip().str.replace('\ufeff', '', regex=True)

# Convert 'REF_DATE' to timestamp format (quarterly)
df['REF_DATE'] = pd.PeriodIndex(df['REF_DATE'], freq='Q').to_timestamp()

# Remove records with missing price index or product category information
df = df.dropna(subset=['VALUE', 'North American Product Classification System (NAPCS)'])

# === MATERIAL CLASSIFICATION ===
# Define a list of keywords associated with fossil fuels
fossil_keywords = ['Diesel', 'Gasoline', 'Fuel oils', 'Crude', 'Petroleum']

# Create a new categorical variable classifying materials as "Fossil Fuels" or "Other Raw Materials"
df['Material_Type'] = df['North American Product Classification System (NAPCS)'].apply(
    lambda x: 'Fossil Fuels' if any(keyword.lower() in x.lower() for keyword in fossil_keywords)
    else 'Other Raw Materials'
)

# === DATA AGGREGATION ===
# Group by quarter and material type to calculate average price index per group
df_grouped = df.groupby(['REF_DATE', 'Material_Type'])['VALUE'].mean().reset_index()

# === VISUALIZATION ===
# Generate a line plot comparing price trends between fossil-based and other materials

plt.figure(figsize=(14, 6))
sns.lineplot(
    data=df_grouped,
    x='REF_DATE',
    y='VALUE',
    hue='Material_Type'
)

# Academic-style formatting
plt.title('Average Price Index: Fossil Fuels vs Other Raw Materials (RMPI)', fontsize=14)
plt.xlabel('Quarter')
plt.ylabel('Price Index (2020=100)')
plt.grid(True)
plt.legend(title='Material Type')
plt.tight_layout()
plt.show()
