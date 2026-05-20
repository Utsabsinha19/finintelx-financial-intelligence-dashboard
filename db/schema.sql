CREATE TABLE dim_company (
    symbol VARCHAR PRIMARY KEY,
    company_name TEXT
);CREATE TABLE dim_company (
    symbol VARCHAR PRIMARY KEY,
    company_name TEXT
);

CREATE TABLE fact_profit_loss (
    symbol VARCHAR,
    year VARCHAR,
    sales FLOAT,
    net_profit FLOAT,
    profit_margin FLOAT,
    PRIMARY KEY (symbol, year)
);

CREATE TABLE fact_balance_sheet (
    symbol VARCHAR,
    year VARCHAR,
    borrowings FLOAT,
    equity_capital FLOAT,
    reserves FLOAT,
    debt_to_equity FLOAT,
    PRIMARY KEY (symbol, year)
);

CREATE TABLE fact_cash_flow (
    symbol VARCHAR,
    year VARCHAR,
    operating_activity FLOAT,
    investing_activity FLOAT,
    free_cash_flow FLOAT,
    PRIMARY KEY (symbol, year)
);

CREATE TABLE dim_year (
    year_id SERIAL PRIMARY KEY,
    year_label VARCHAR
);

CREATE TABLE fact_profit_loss (
    symbol VARCHAR,
    year_label VARCHAR,
    sales FLOAT,
    net_profit FLOAT,
    PRIMARY KEY (symbol, year_label)
);

CREATE TABLE fact_balance_sheet (
    symbol VARCHAR,
    year_label VARCHAR,
    total_assets FLOAT,
    borrowings FLOAT,
    PRIMARY KEY (symbol, year_label)
);

CREATE TABLE fact_cash_flow (
    symbol VARCHAR,
    year_label VARCHAR,
    operating_activity FLOAT,
    investing_activity FLOAT,
    PRIMARY KEY (symbol, year_label)
);