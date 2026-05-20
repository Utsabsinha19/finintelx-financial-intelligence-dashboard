import pandas as pd

df = pd.read_excel("data/raw/profitandloss.xlsx")
print(df.columns)
print(df.head())
print(df.info())

# Null handling
df.replace(['NULL', 'Null', '-', ''], pd.NA, inplace=True)
# Clean year
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

df['year'] = df['year'].apply(extract_year)

# Clean numeric columns
for col in df.columns:
    if df[col].dtype == 'object':
        df[col] = (df[col]
                   .str.replace(",", "", regex=False)
                   .str.replace("%", "", regex=False)
        )

df.to_csv("data/clean/profitandloss.csv", index=False)