import pandas as pd
from sqlalchemy import create_engine

# 🔹 UPDATE PASSWORD
engine = create_engine("postgresql://postgres:9543@localhost:5432/financial_db")


# -------------------------------
# CLEAN FUNCTION
# -------------------------------
def clean_symbol(df):
    df["symbol"] = df["symbol"].astype(str).str.strip().str.upper()
    return df


# -------------------------------
# LOAD COMPANIES (WITH SYMBOL)
# -------------------------------
def load_companies():
    df = pd.read_csv("data/clean/companies.csv", skiprows=1)
    df.columns = df.columns.str.strip().str.lower()

    df = df.rename(columns={"id": "symbol"})

    df["company_name"] = df["company_name"].str.strip()
    df = clean_symbol(df)

    df = df[["symbol", "company_name"]].dropna().drop_duplicates()

    existing = pd.read_sql("SELECT company_name FROM company", engine)
    df = df[~df["company_name"].isin(existing["company_name"])]

    if len(df) > 0:
        df.to_sql("company", engine, if_exists="append", index=False)

    print(f"✅ company loaded ({len(df)} rows)")


# -------------------------------
# GENERIC INSERT FUNCTION
# -------------------------------
def insert_with_symbol(df, table_name):
    company_df = pd.read_sql("SELECT * FROM company", engine)

    df = clean_symbol(df)
    company_df = clean_symbol(company_df)

    df = df.merge(company_df, on="symbol", how="left")

    missing = df["company_id"].isna().sum()
    if missing > 0:
        print(f"⚠️ {missing} rows missing company_id in {table_name}")

    df = df.dropna(subset=["company_id"])
    df = df.drop_duplicates()

    # ❗ KEEP ONLY REQUIRED COLUMNS
    if table_name == "balance_sheet":
        df = df[["company_id", "year", "equity_capital", "reserves", "borrowings", "total_assets"]]

    elif table_name == "profit_loss":
        df = df[["company_id", "year", "revenue", "expenses", "profit"]]

    elif table_name == "cash_flow":
        df = df[["company_id", "year", "cash_in", "cash_out", "net_cash"]]

    elif table_name == "analysis":
        df = df[["company_id"]]

    elif table_name == "documents":
        df = df[["company_id", "year"]]

    elif table_name == "pros_cons":
        df = df[["company_id"]]

    df = df.dropna()
    df = df.drop_duplicates()

    df.to_sql(table_name, engine, if_exists="append", index=False)

    print(f"✅ {table_name} loaded ({len(df)} rows)")


# -------------------------------
# BALANCE SHEET
# -------------------------------
def load_balance_sheet():
    df = pd.read_csv("data/clean/balancesheet.csv", skiprows=1, header=None)

    df = df.iloc[:, :6]
    df.columns = ["symbol", "year", "equity_capital", "reserves", "borrowings", "total_assets"]

    return df


# -------------------------------
# PROFIT & LOSS
# -------------------------------
def load_profit_loss():
    df = pd.read_csv("data/clean/profitandloss.csv", skiprows=1, header=None)

    df = df.iloc[:, :5]
    df.columns = ["symbol", "year", "revenue", "expenses", "profit"]

    return df


# -------------------------------
# CASH FLOW
# -------------------------------
def load_cash_flow():
    df = pd.read_csv("data/clean/cashflow.csv", skiprows=1, header=None)

    df = df.iloc[:, :5]
    df.columns = ["symbol", "year", "cash_in", "cash_out", "net_cash"]

    return df


# -------------------------------
# ANALYSIS
# -------------------------------
def load_analysis():
    df = pd.read_csv("data/clean/analysis.csv", skiprows=1, header=None)

    df = df.iloc[:, :1]
    df.columns = ["symbol"]

    return df


# -------------------------------
# DOCUMENTS
# -------------------------------
def load_documents():
    df = pd.read_csv("data/clean/documents.csv", skiprows=1)
    df.columns = df.columns.str.strip().str.lower()

    df = df.rename(columns={"company_id": "symbol", "year": "year"})
    return df


# -------------------------------
# PROS & CONS
# -------------------------------
def load_pros_cons():
    df = pd.read_csv("data/clean/prosandcons.csv", skiprows=1)
    df.columns = df.columns.str.strip().str.lower()

    df = df.rename(columns={"company_id": "symbol"})
    return df


# -------------------------------
# MAIN PIPELINE
# -------------------------------
if __name__ == "__main__":

    print("🚀 STARTING PIPELINE...\n")

    load_companies()

    insert_with_symbol(load_balance_sheet(), "balance_sheet")
    insert_with_symbol(load_profit_loss(), "profit_loss")
    insert_with_symbol(load_cash_flow(), "cash_flow")
    insert_with_symbol(load_analysis(), "analysis")
    insert_with_symbol(load_documents(), "documents")
    insert_with_symbol(load_pros_cons(), "pros_cons")

    print("\n✅ ALL DATA LOADED SUCCESSFULLY")