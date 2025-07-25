

import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import os
from datetime import datetime

# ================================
# 1. SETUP
# ================================

# Create folders
os.makedirs("data", exist_ok=True)
os.makedirs("macro_charts", exist_ok=True)
os.makedirs("charts", exist_ok=True)

# Date range
start_date = "2010-01-01"
end_date = "2024-01-01"

# Macro indicators from FRED
macro_series = {
    "FEDFUNDS": "Federal_Funds_Rate",
    "DGS10": "10Y_Treasury_Rate",
    "CPIAUCSL": "CPI",
    "UNRATE": "Unemployment_Rate",
    "GDP": "GDP",
    "PCECC96": "PCE",
    "M2SL": "M2_Money_Supply",
    "UMCSENT": "Consumer_Sentiment"
}

# ================================
# 2. DOWNLOAD MACRO DATA
# ================================

macro_df = pd.DataFrame()

for code, name in macro_series.items():
    try:
        data = web.DataReader(code, "fred", start_date, end_date)
        data.columns = [name]
        macro_df = pd.concat([macro_df, data], axis=1)

        # Save individual chart
        plt.figure(figsize=(10, 4))
        plt.plot(data.index, data[name], label=name)
        plt.title(name)
        plt.xlabel("Date")
        plt.ylabel(name)
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"macro_charts/{name}.png")
        plt.close()

        print(f"{name} downloaded and chart saved.")
    except Exception as e:
        print(f"❌ Error downloading {code}: {e}")

macro_df.to_csv("data/macro_data.csv")
print("✅ All macro data saved to 'data/macro_data.csv'.")

# ================================
# 3. LOAD MANUAL SPY CSV (2 headers)
# ================================

try:
    spy = pd.read_csv("data/spy_data.csv", skiprows=1, index_col=0, parse_dates=True)
    spy.columns = ["SPY_Adj_Close"]
    spy.index.name = "Date"
    print("✅ SPY data cleaned and loaded.")
except Exception as e:
    raise ValueError(f"❌ Failed to load SPY CSV: {e}")

# ================================
# 4. MERGE MACRO + SPY
# ================================

try:
    combined_df = macro_df.merge(spy, left_index=True, right_index=True, how="inner")
    combined_df.dropna(inplace=True)
    combined_df.to_csv("data/combined_macro_spy.csv")
    print("✅ Merged macro + SPY data saved to 'data/combined_macro_spy.csv'.")
except Exception as e:
    raise ValueError(f"❌ Failed to merge datasets: {e}")

# ================================
# 5. COMBINED MACRO DASHBOARD CHART
# ================================

fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(18, 16))
axes = axes.flatten()

for i, column in enumerate(macro_df.columns):
    axes[i].plot(macro_df.index, macro_df[column], label=column, color='navy')
    axes[i].set_title(column)
    axes[i].grid(True)
    axes[i].tick_params(axis='x', rotation=45)

# Clean extra subplots
for j in range(len(macro_df.columns), len(axes)):
    fig.delaxes(axes[j])

fig.suptitle("📊 Macro Indicators Overview", fontsize=20)
fig.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig("charts/macro_dashboard_combined.png")
plt.close()
print("✅ Combined macro dashboard chart saved.")


# ================================
# 5. EXPORT EACH MACRO SERIES TO CSV
# ================================

import os

# Create a folder to store individual macro CSVs
os.makedirs("data/macro_individual_csvs", exist_ok=True)

# Save each macro series to a separate CSV
for column in macro_df.columns:
    output_path = os.path.join("data/macro_individual_csvs", f"{column}.csv")
    macro_df[[column]].dropna().to_csv(output_path)

# Save SPY price data separately
spy_df = pd.read_csv("data/spy_data.csv", index_col=0, parse_dates=True)
spy_df.to_csv("data/macro_individual_csvs/SPY_Adj_Close.csv")

print("✅ All macro indicators and SPY data exported to 'data/macro_individual_csvs/'.")





import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import os

# Create output folder if not exists
os.makedirs("charts", exist_ok=True)

# Load merged data
combined_df = pd.read_csv("data/combined_macro_spy.csv", index_col=0, parse_dates=True)

# ================================
# 1. Fixed Multi-Plot Macro Dashboard
# ================================
fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(18, 16))
axes = axes.flatten()

macro_columns = [col for col in combined_df.columns if col != "SPY_Adj_Close"]

for i, column in enumerate(macro_columns):
    axes[i].plot(combined_df.index, combined_df[column], label=column, color='navy')
    axes[i].set_title(column)
    axes[i].grid(True)
    axes[i].tick_params(axis='x', rotation=45)

# Remove any unused subplots
for j in range(len(macro_columns), len(axes)):
    fig.delaxes(axes[j])

fig.suptitle("📊 Macro Indicators Overview", fontsize=20)
fig.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig("charts/macro_dashboard_combined.png")
plt.close()
print("✅ Fixed macro dashboard chart saved.")

# ================================
# 2. Normalized Line Chart (Z-Scores)
# ================================
from sklearn.preprocessing import StandardScaler

# Drop missing values across all columns
clean_df = combined_df.dropna()

# Confirm non-empty
if clean_df.shape[0] == 0:
    raise ValueError("❌ No data left after dropping NaNs. Check date alignment of SPY and macro data.")

# Z-score normalization
scaler = StandardScaler()
normalized_data = scaler.fit_transform(clean_df)

# Convert back to DataFrame
normalized_df = pd.DataFrame(normalized_data, index=clean_df.index, columns=clean_df.columns)

# Plot all normalized indicators including SPY
plt.figure(figsize=(16, 6))
for column in normalized_df.columns:
    plt.plot(normalized_df.index, normalized_df[column], label=column)

plt.title("Normalized Macro Indicators + S&P 500")
plt.xlabel("Date")
plt.ylabel("Z-Score Normalized Values")
plt.legend(loc="best")
plt.grid(True)
plt.tight_layout()
plt.savefig("charts/macro_plus_sp500_normalized.png")
plt.close()
print("✅ Normalized macro + SPY chart saved.")






