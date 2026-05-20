import pandas as pd
import os

CLEAN_PATH = "data/clean/"

# Profit & Loss Features
pl = pd.read_csv(f"{CLEAN_PATH}profitandloss.csv")

pl['sales'] = pd.to_numeric(pl['sales'], errors='coerce')
pl['net_profit'] = pd.to_numeric(pl['net_profit'], errors='coerce')

pl['profit_margin'] = (pl['net_profit'] / pl['sales']) * 100

pl.to_csv(f"{CLEAN_PATH}profitandloss.csv", index=False)


# Balance Sheet Features
bs = pd.read_csv(f"{CLEAN_PATH}balancesheet.csv")

bs['borrowings'] = pd.to_numeric(bs['borrowings'], errors='coerce')
bs['equity_capital'] = pd.to_numeric(bs['equity_capital'], errors='coerce')
bs['reserves'] = pd.to_numeric(bs['reserves'], errors='coerce')

bs['debt_to_equity'] = bs['borrowings'] / (bs['equity_capital'] + bs['reserves'])

bs.to_csv(f"{CLEAN_PATH}balancesheet.csv", index=False)


# Cash Flow Features
cf = pd.read_csv(f"{CLEAN_PATH}cashflow.csv")

cf['operating_activity'] = pd.to_numeric(cf['operating_activity'], errors='coerce')
cf['investing_activity'] = pd.to_numeric(cf['investing_activity'], errors='coerce')

cf['free_cash_flow'] = cf['operating_activity'] + cf['investing_activity']

cf.to_csv(f"{CLEAN_PATH}cashflow.csv", index=False)

print("Feature engineering completed")