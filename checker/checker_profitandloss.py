import pandas as pd
import numpy as np

df = pd.read_excel("data/raw/profitandloss.xlsx", header=1)

# Clean column names
df.columns = df.columns.str.strip().str.lower()

# Rename
df.rename(columns={'company_id': 'symbol'}, inplace=True)

# Drop id
df.drop(columns=['id'], inplace=True)

# Extract year
df['year'] = df['year'].str.extract(r'(\d{4})')

# Feature Engineering
df['net_profit_margin'] = (df['net_profit'] / df['sales']) * 100
df['expense_ratio'] = (df['expenses'] / df['sales']) * 100
df['interest_coverage'] = df['operating_profit'] / df['interest']

# Final check
print(df.info())
print(df.head())

# Save
df.to_csv("data/clean/profitandloss.csv", index=False)

print("✅ FACT TABLE READY")