
import os
import pandas as pd
import re
import statsmodels.api as sm

# === PATHS ===
base_dir = r"C:/Users/ty10b/Dropbox/CRAFT/7.24.2025 - Finance Forecast"
summary_dir = os.path.join(base_dir, "data")
output_csv = os.path.join(base_dir, "data/summary_table.csv")

# === LIST OF MACRO FACTORS ===
macro_factors = [
    "10Y",
    "AllMacros",
    "ConsumerSentiment",
    "CPI",
    "FedFunds",
    "GDP",
    "M2",
    "Unemployment"
]

# === PARSE SUMMARY FILES ===
summary_data = []

for factor in macro_factors:
    file_path = os.path.join(summary_dir, f"regression_summary_SPY_vs_{factor}.txt")
    
    with open(file_path, "r") as f:
        content = f.read()

    # R-squared
    r2_match = re.search(r"R-squared:\s+([0-9.]+)", content)
    r_squared = float(r2_match.group(1)) if r2_match else None

    # Coefficient (2nd row under coef column)
    coef_match = re.findall(r"\n[\s\w]+\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)", content)
    coef = float(coef_match[1][0]) if coef_match and len(coef_match) > 1 else None  # Row 2 = macro variable

    # P-value (5th column in the same row)
    p_value = float(coef_match[1][4]) if coef_match and len(coef_match) > 1 else None

    summary_data.append({
        "Macro_Var": factor,
        "R_squared": r_squared,
        "Coefficient": coef,
        "P_value": p_value
    })

# === SAVE TO CSV ===
summary_df = pd.DataFrame(summary_data)
summary_df.to_csv(output_csv, index=False)
print(f"✅ Summary table saved to: {output_csv}")

