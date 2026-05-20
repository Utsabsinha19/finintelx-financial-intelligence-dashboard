import pandas as pd
import numpy as np

# ✅ Step 1: Read file (skip title row)
df = pd.read_excel("data/raw/balancesheet.xlsx", header=1)

# ✅ Step 2: Clean column names
df.columns = df.columns.str.strip().str.lower()

print("Columns BEFORE rename:", df.columns)

# ✅ Step 3: Rename correctly (IMPORTANT)
df.rename(columns={
    'company_': 'symbol',
    'reserve': 'reserves'
}, inplace=True)

print("Columns AFTER rename:", df.columns)

# ✅ Step 4: Check symbol column
print(df[['symbol']].head())

# ✅ Step 5: Drop id
df.drop(columns=['id'], inplace=True)

# ✅ Step 6: Extract year
df['year'] = df['year'].str.extract(r'(\d{4})').astype(int)

# ✅ Step 7: Replace nulls
df.replace(['NULL', 'Null', '-', ''], np.nan, inplace=True)

# ✅ Step 8: Convert numeric columns
exclude_cols = ['symbol', 'year']

for col in df.columns:
    if col not in exclude_cols:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "", regex=False)
        )
        df[col] = pd.to_numeric(df[col], errors='coerce')

# -------------------------
# 🔥 FEATURE ENGINEERING
# -------------------------

# Debt to Equity
df['debt_to_equity'] = df['borrowings'] / (df['equity_capital'] + df['reserves'])

# Equity Ratio
df['equity_ratio'] = (df['equity_capital'] + df['reserves']) / df['total_assets']

# Handle infinity
df.replace([np.inf, -np.inf], np.nan, inplace=True)

# -------------------------
# ✅ VALIDATION
# -------------------------

print("Nulls in symbol:", df['symbol'].isnull().sum())
print("Duplicate rows:", df.duplicated(subset=['symbol', 'year']).sum())

print(df.head())
print(df.info())

# ✅ Save clean file
df.to_csv("data/clean/balancesheet.csv", index=False)

print("🔥 BALANCE SHEET PERFECTLY CLEANED")