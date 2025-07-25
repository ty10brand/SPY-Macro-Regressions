

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import os

# === PATHS ===
base_dir = base_path = r"C:/your/local/path"
macro_dir = os.path.join(base_dir, "data/macro_individual_csvs")
spy_path = os.path.join(macro_dir, "SPY_Adj_Close.csv")
summary_output_path = os.path.join(base_dir, "data/regression_summary_SPY_vs_AllMacros.txt")
csv_output_path = os.path.join(base_dir, "data/regression_data_SPY_vs_AllMacros.csv")

# === Load SPY ===
spy_df = pd.read_csv(spy_path, index_col=0, parse_dates=True)
spy_df.index = pd.to_datetime(spy_df.index, errors='coerce')
spy_df["SPY_Adj_Close"] = pd.to_numeric(spy_df["SPY_Adj_Close"], errors="coerce")
spy_df.dropna(inplace=True)

spy_monthly = spy_df.resample("ME").last()
spy_monthly["Log_Returns"] = np.log(spy_monthly["SPY_Adj_Close"] / spy_monthly["SPY_Adj_Close"].shift(1))
spy_monthly.dropna(inplace=True)

# === Load All Macro Variables ===
macro_files = {
    "10Y": "10Y_Treasury_Rate.csv",
    "ConsumerSentiment": "Consumer_Sentiment.csv",
    "CPI": "CPI.csv",
    "FedFunds": "Federal_Funds_Rate.csv",
    "GDP": "GDP.csv",
    "M2": "M2_Money_Supply.csv",
    "Unemployment": "Unemployment_Rate.csv"
}

macro_data = []
for var_name, filename in macro_files.items():
    df = pd.read_csv(os.path.join(macro_dir, filename), index_col=0, parse_dates=True)
    df.index = pd.to_datetime(df.index, errors='coerce')
    df = df.resample("ME").last().dropna()
    df.columns = [var_name]
    macro_data.append(df)

# === Combine all macro into one dataframe ===
macro_df = pd.concat(macro_data, axis=1).dropna()

# === Merge with SPY log returns ===
merged_df = pd.merge(spy_monthly[["Log_Returns"]], macro_df, left_index=True, right_index=True, how="inner")

# === Regression ===
X = sm.add_constant(merged_df.drop(columns=["Log_Returns"]))
y = merged_df["Log_Returns"]
model = sm.OLS(y, X).fit()

# Add predictions
merged_df["Predicted_Return"] = model.predict(X)
merged_df["Residual"] = y - merged_df["Predicted_Return"]

# === Save Data ===
merged_df.to_csv(csv_output_path)
print(f"✅ Merged data with predictions saved to: {csv_output_path}")

# === Save Summary ===
with open(summary_output_path, "w") as f:
    f.write(model.summary().as_text())
print(f"✅ Regression summary saved to: {summary_output_path}")

# === Optional: Print R-squared and key metrics ===
print(model.summary())

# === PLOT: Actual vs Predicted Returns ===
plot_output_path = os.path.join(base_dir, "charts/regression_SPY_vs_AllMacros.png")

plt.figure(figsize=(10, 6))
plt.plot(merged_df.index, merged_df["Log_Returns"], label="Actual", color='blue', linewidth=2)
plt.plot(merged_df.index, merged_df["Predicted_Return"], label="Predicted", color='red', linestyle="--", linewidth=2)
plt.title("Multiple Linear Regression: SPY Returns vs All Macroeconomic Factors")
plt.xlabel("Date")
plt.ylabel("Monthly Log Returns")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(plot_output_path)
plt.close()
print(f"✅ Plot saved to: {plot_output_path}")



