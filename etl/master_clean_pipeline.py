import pandas as pd
import numpy as np
import os

RAW_PATH = "data/raw/"
CLEAN_PATH = "data/clean/"

os.makedirs(CLEAN_PATH, exist_ok=True)

# -------------------------
# 🔧 COMMON FUNCTIONS
# -------------------------

def standardize_columns(df):
    df.columns = df.columns.str.strip().str.lower()
    return df

def standardize_symbol(df):
    if 'company_' in df.columns:
        df.rename(columns={'company_': 'symbol'}, inplace=True)
    elif 'company_id' in df.columns:
        df.rename(columns={'company_id': 'symbol'}, inplace=True)
    return df

def extract_year(df):
    if 'year' in df.columns:
        df['year'] = df['year'].astype(str).str.extract(r'(\d{4})')
    return df

def clean_nulls(df):
    df.replace(['NULL', 'Null', '-', ''], np.nan, inplace=True)
    return df

def convert_numeric(df, exclude_cols):
    for col in df.columns:
        if col not in exclude_cols:
            df[col] = (
                df[col].astype(str)
                .str.replace(",", "", regex=False)
                .str.replace("%", "", regex=False)
            )
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def handle_infinity(df):
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    return df

# -------------------------
# 📊 DATASET-SPECIFIC LOGIC
# -------------------------

def process_profitandloss():
    df = pd.read_excel(RAW_PATH + "profitandloss.xlsx", header=1)

    df = standardize_columns(df)
    df = standardize_symbol(df)
    df = clean_nulls(df)
    df = extract_year(df)

    df.drop(columns=['id'], inplace=True)

    df = convert_numeric(df, exclude_cols=['symbol', 'year'])

    # 🔥 Features
    df['net_profit_margin'] = (df['net_profit'] / df['sales']) * 100
    df['expense_ratio'] = (df['expenses'] / df['sales']) * 100
    df['interest_coverage'] = np.where(
        df['interest'] == 0,
        np.nan,
        df['operating_profit'] / df['interest']
    )

    df = handle_infinity(df)

    df.to_csv(CLEAN_PATH + "profitandloss.csv", index=False)
    print("✅ profitandloss done")


def process_balancesheet():
    df = pd.read_excel(RAW_PATH + "balancesheet.xlsx", header=1)

    df = standardize_columns(df)
    df = standardize_symbol(df)
    df = clean_nulls(df)
    df = extract_year(df)

    df.rename(columns={'reserve': 'reserves'}, inplace=True)

    df.drop(columns=['id'], inplace=True)

    df = convert_numeric(df, exclude_cols=['symbol', 'year'])

    # 🔥 Features
    df['debt_to_equity'] = df['borrowings'] / (df['equity_capital'] + df['reserves'])
    df['equity_ratio'] = (df['equity_capital'] + df['reserves']) / df['total_assets']

    df = handle_infinity(df)

    df.to_csv(CLEAN_PATH + "balancesheet.csv", index=False)
    print("✅ balancesheet done")


def process_cashflow():
    df = pd.read_excel(RAW_PATH + "cashflow.xlsx", header=1)

    df = standardize_columns(df)
    df = standardize_symbol(df)
    df = clean_nulls(df)
    df = extract_year(df)

    df.drop(columns=['id'], inplace=True)

    df = convert_numeric(df, exclude_cols=['symbol', 'year'])

    # 🔥 Feature
    df['free_cash_flow'] = df['operating_activity'] + df['investing_activity']

    df = handle_infinity(df)

    df.to_csv(CLEAN_PATH + "cashflow.csv", index=False)
    print("✅ cashflow done")


def process_analysis():
    df = pd.read_excel(RAW_PATH + "analysis.xlsx", header=1)

    df = standardize_columns(df)
    df = standardize_symbol(df)
    df = clean_nulls(df)

    df.drop(columns=['id'], inplace=True)

    df = convert_numeric(df, exclude_cols=['symbol'])

    df.to_csv(CLEAN_PATH + "analysis.csv", index=False)
    print("✅ analysis done")


def process_companies():
    df = pd.read_excel(RAW_PATH + "companies.xlsx")

    df = standardize_columns(df)
    df = standardize_symbol(df)

    df.to_csv(CLEAN_PATH + "companies.csv", index=False)
    print("✅ companies done")


def process_proscons():
    df = pd.read_excel(RAW_PATH + "prosandcons.xlsx")

    df = standardize_columns(df)
    df = standardize_symbol(df)

    df.to_csv(CLEAN_PATH + "prosandcons.csv", index=False)
    print("✅ prosandcons done")


def process_documents():
    df = pd.read_excel(RAW_PATH + "documents.xlsx")

    df = standardize_columns(df)
    df = standardize_symbol(df)

    df.to_csv(CLEAN_PATH + "documents.csv", index=False)
    print("✅ documents done")


# -------------------------
# 🚀 RUN ALL
# -------------------------

if __name__ == "__main__":
    process_profitandloss()
    process_balancesheet()
    process_cashflow()
    process_analysis()
    process_companies()
    process_proscons()
    process_documents()

    print("\n🔥 ALL DATA CLEANED SUCCESSFULLY")