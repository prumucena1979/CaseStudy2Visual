# Import necessary libraries for data processing and dual-axis visualization
import pandas as pd
import matplotlib.pyplot as plt

# === DATA INGESTION: CPI (Consumer Price Index) ===
# Load monthly CPI data from the Bank of Canada dataset
df_cpi = pd.read_csv(r"C:\Users\FabiodosSantosPrumuc\Desktop\meusdatasets\CPI_MONTHLY.csv")

# Convert 'date' to datetime object for time manipulation
df_cpi['date'] = pd.to_datetime(df_cpi['date'])

# Filter data to include only observations from 1997 onward
df_cpi = df_cpi[df_cpi['date'].dt.year >= 1997]

# Convert monthly dates to quarterly periods, then to string for merging
df_cpi['quarter_str'] = df_cpi['date'].dt.to_period('Q').astype(str)

# Aggregate CPI by quarter: compute average CPI change within each quarter
df_cpi_quarterly = df_cpi.groupby('quarter_str')['STATIC_TOTALCPICHANGE'].mean().reset_index()

# === DATA INGESTION: GDP ===
# Load quarterly GDP data from Statistics Canada
df_gdp = pd.read_csv(r"C:\Users\FabiodosSantosPrumuc\Desktop\meusdatasets\36100434.csv", encoding='latin1', low_memory=False)

# Handle any corrupted or misencoded column names (e.g., BOM character)
if 'ï»¿REF_DATE' in df_gdp.columns:
    df_gdp.rename(columns={'ï»¿REF_DATE': 'REF_DATE'}, inplace=True)
df_gdp.columns = df_gdp.columns.str.strip()

# Convert REF_DATE to quarterly period string format for compatibility with CPI
df_gdp['quarter_str'] = pd.PeriodIndex(df_gdp['REF_DATE'], freq='Q').astype(str)

# (Optional) Display unique industry classifications for exploratory purposes
print("\n🔍 Unique industry names in GDP dataset:")
print(df_gdp['North American Industry Classification System (NAICS)'].dropna().unique()[:10])

# Filter for "All industries" to capture the aggregate GDP value
# This avoids disaggregated views by sector and ensures alignment with national inflation data
df_gdp = df_gdp[
    df_gdp['North American Industry Classification System (NAICS)']
    .str.contains('All industries', case=False, na=False)
]

# Group by quarter and sum GDP values (in chained 2017 dollars)
df_gdp = df_gdp.groupby('quarter_str')['VALUE'].sum().reset_index()
df_gdp = df_gdp.rename(columns={'VALUE': 'GDP'})

# === DATA MERGING ===
# Merge CPI and GDP datasets using the standardized 'quarter_str' as key
df_merged = pd.merge(df_gdp, df_cpi_quarterly, on='quarter_str')

# Rename the CPI column for clarity
df_merged = df_merged.rename(columns={'STATIC_TOTALCPICHANGE': 'CPI'})

# Convert quarter_str to timestamp for better visualization on x-axis
df_merged['quarter_str'] = pd.PeriodIndex(df_merged['quarter_str'], freq='Q').to_timestamp()

# === DATA VISUALIZATION: Dual-Axis Line Chart ===
# Create a figure with two y-axes to display GDP and CPI together

fig, ax1 = plt.subplots(figsize=(14, 6))

# Plot GDP on the primary y-axis (left)
color = 'tab:blue'
ax1.set_xlabel('Quarter')
ax1.set_ylabel('GDP (Millions, Chained 2017 $)', color=color)
ax1.plot(df_merged['quarter_str'], df_merged['GDP'], color=color, label='GDP')
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_xticks(df_merged['quarter_str'][::4])
ax1.set_xticklabels(df_merged['quarter_str'][::4].dt.strftime('%Y-Q%q'), rotation=45)

# Plot CPI on the secondary y-axis (right)
ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Inflation Rate (%)', color=color)
ax2.plot(df_merged['quarter_str'], df_merged['CPI'], color=color, linestyle='--', label='CPI')
ax2.tick_params(axis='y', labelcolor=color)

# Chart title and layout enhancements
plt.title('Graph 3 – Quarterly Inflation vs GDP (Canada)', fontsize=14)
plt.grid(True)
plt.tight_layout()
plt.show()

# Pause to keep the chart open in CLI execution
input("✅ Pressione Enter to close the chart...")
