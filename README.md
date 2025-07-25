# SPY-Macro-Regressions
Linear Regression of Macroeconomic metrics and the S&amp;P 500 for past 10 years.

# 📈 S&P 500 vs Macroeconomic Indicators: Regression Analysis Project

Welcome! This is my first public GitHub project where I explore the relationship between the S&P 500 and key U.S. macroeconomic indicators using Python and linear regression.

---

## Project Overview

This project investigates whether common economic variables can explain or predict monthly returns of the S&P 500 index. For each factor, I ran individual linear regressions and visualized the results. I then combined them into a multiple linear regression model to see how they perform together.

---

## Methodology

- **Data Sources:** Historical time series from macroeconomic indicators (e.g., CPI, M2, Fed Funds Rate, GDP, etc.) and SPY adjusted close prices
- **Tools Used:**  
  - `pandas` for data cleaning  
  - `statsmodels` for regression  
  - `matplotlib` for visualizations  
  - `os` for path management

- **Steps:**
  1. Cleaned and resampled data to monthly frequency
  2. Computed log returns for SPY
  3. Ran individual regressions: `SPY_log_returns ~ Macro_Variable`
  4. Created regression plots and summary CSVs
  5. Built a multiple linear regression model combining all factors

---


---

## Sample Output

Each chart shows a scatterplot of S&P log returns vs the macro variable, with a red regression line overlay. Summary CSVs and text files include R-squared, p-values, and regression coefficients.

---

## What’s Next?

- Add non-linear models (e.g., XGBoost)
- Try classification or time series forecasting
- Explore agent-based or reinforcement learning models


---

## About Me

I'm Tyler Brand, a PhD student studying GIS and logistics optimization. This repo reflects my curiosity for macroeconomics and data science. I believe in learning by doing — and this is part of that journey.

---

## Why I Built This

Not because I want to become a quant. I did it to sharpen my skills, create something from scratch, and keep pushing the boundaries of what I can build with Python and data. Just a small brick in a much bigger foundation.

---

Thanks for checking it out!  
– Tyler



