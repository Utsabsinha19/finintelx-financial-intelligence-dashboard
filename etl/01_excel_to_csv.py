import pandas as pd
import os

RAW_PATH = "data/raw/"
INTERIM_PATH = "data/interim/"

files = [
    "companies",
    "balancesheet",
    "profitandloss",
    "cashflow",
    "analysis",
    "prosandcons",
    "documents"
]

os.makedirs(INTERIM_PATH, exist_ok=True)

for file in files:
    df = pd.read_excel(f"{RAW_PATH}{file}.xlsx")
    df.to_csv(f"{INTERIM_PATH}{file}.csv", index=False)
    print(f"{file} converted")