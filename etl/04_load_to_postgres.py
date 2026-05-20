from sqlalchemy import create_engine
import pandas as pd

# DATABASE CONNECTION
engine = create_engine(
    "postgresql://postgres:ut.si%4023@localhost:5432/financial_db"
)

# LOAD FUNCTION
def load(file, table):
    df = pd.read_csv(file)

    df.to_sql(
        table,
        engine,
        if_exists="replace",
        index=False
    )

    print(f"{table} loaded successfully")


# LOAD TABLES

load("data/clean/companies.csv", "dim_company")

load("data/clean/profitandloss.csv", "fact_profit_loss")

load("data/clean/balancesheet.csv", "fact_balance_sheet")

load("data/clean/cashflow.csv", "fact_cash_flow")

load("data/clean/analysis.csv", "fact_analysis")

load("data/clean/prosandcons.csv", "fact_pros_cons")

load("data/clean/documents.csv", "fact_documents")