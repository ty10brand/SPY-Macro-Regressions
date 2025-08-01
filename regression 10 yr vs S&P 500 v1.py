import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import os

# === PATHS ===
base_dir = r"C:/your/local/path"
spy_path = os.path.join(base_dir, "data/macro_individual_csvs/SPY_Adj_Close.csv")
macro_path = os.path.join(base_dir, "data/macro_individual_csvs/10Y_Treasury_Rate.csv")
plot_output = os.path.join(base_dir, "charts/regression_SPY_vs_10Y.png")
csv_output = os.path.join(base_dir, "data/regression_output_SPY_vs_10Y.csv")

# === LOAD SPY ===
spy_df = pd.read_csv(spy_path, index_col=0, parse_dates=True)
spy_df.index = pd.to_datetime(spy_df.index, errors='coerce')
spy_df["SPY_Adj_Close"] = pd.to_numeric(spy_df["SPY_Adj_Close"], errors="coerce")
spy_df.dropna(inplace=True)

# Resample monthly & log returns
spy_monthly = spy_df.resample("ME").last()
spy_monthly["Log_Returns"] = np.log(spy_monthly["SPY_Adj_Close"] / spy_monthly["SPY_Adj_Close"].shift(1))
spy_monthly.dropna(inplace=True)

# === LOAD MACRO VARIABLE ===
macro_df = pd.read_csv(macro_path, index_col=0, parse_dates=True)
macro_df.index = pd.to_datetime(macro_df.index, errors='coerce')
macro_df.columns = ["Macro"]
macro_df = macro_df.resample("ME").last().dropna()

# === MERGE & REGRESSION ===
merged_df = pd.merge(spy_monthly[["Log_Returns"]], macro_df, left_index=True, right_index=True, how="inner")

X = sm.add_constant(merged_df["Macro"])
y = merged_df["Log_Returns"]
model = sm.OLS(y, X).fit()

print(model.summary())

# === EXPORT MERGED CSV ===
merged_df.to_csv(csv_output)
print(f"✅ Merged regression data saved to: {csv_output}")

# === PLOT ===
plt.figure(figsize=(10, 6))
plt.scatter(merged_df["Macro"], merged_df["Log_Returns"], alpha=0.6)
plt.plot(merged_df["Macro"], model.predict(X), color='red', label='Regression Line')
plt.xlabel("10Y Treasury Rate")
plt.ylabel("S&P 500 Monthly Log Returns")
plt.title("Linear Regression: SPY Returns vs 10Y Treasury Rate")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(plot_output)
plt.close()
print(f"✅ Regression plot saved to: {plot_output}")


