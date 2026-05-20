import pandas as pd
import numpy as np
import os

INTERIM_PATH = "data/interim/"
CLEAN_PATH = "data/clean/"

os.makedirs(CLEAN_PATH, exist_ok=True)

def clean_numeric(col):
    return (
        col.astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("%", "", regex=False)
    )

def extract_year(year):
    if pd.isna(year):
        return None
    year = str(year)

    if "TTM" in year:
        return "TTM"

    digits = ''.join(filter(str.isdigit, year))
    if len(digits) >= 4:
        return digits[-4:]
    return None

def clean_file(file):
    df = pd.read_csv(f"{INTERIM_PATH}{file}.csv")

    # Null handling
    df.replace(['NULL', 'Null', '-', ''], np.nan, inplace=True)

    # Clean year
    if 'year' in df.columns:
        df['year'] = df['year'].apply(extract_year)

    # Clean numeric columns
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = clean_numeric(df[col])

    return df

files = [
    "companies",
    "balancesheet",
    "profitandloss",
    "cashflow",
    "analysis",
    "prosandcons",
    "documents"
]

for file in files:
    df = clean_file(file)
    df.to_csv(f"{CLEAN_PATH}{file}.csv", index=False)
    print(f"{file} cleaned")