import pandas as pd
nav_history = pd.read_csv("C:/Users/user/mutual-fund-analytics/data/raw/02_nav_history.csv")
print(nav_history.columns.tolist())
print(nav_history.dtypes)
print(nav_history.shape)
#  Parse dates to datetime
nav_history['date']=pd.to_datetime(nav_history['date'])
#  Sort by amfi_code + date
nav_history=nav_history.sort_values(by=['amfi_code','date'])
#  Remove duplicates
nav_history=nav_history.drop_duplicates(subset=['amfi_code','date'])
#  Validate NAV > 0 (remove invalid rows)
invalid_nav=nav_history[nav_history['nav'] <=0]
print("invalid nav count:",len(invalid_nav))
nav_history=nav_history[nav_history['nav']>0]
# Forward-fill missing NAV for holidays/weekends (creates daily rows per fund)
nav_history = nav_history.set_index('date')
nav_history = nav_history.groupby('amfi_code')['nav'].apply(
    lambda x: x.asfreq('D').ffill()
).reset_index()

print("After cleaning:", nav_history.shape)
print(nav_history.head(10))

nav_history.to_csv("C:/Users/user/mutual-fund-analytics/data/processed/02_nav_history_cleaned.csv", index=False)
print("Saved!")


print("\n" + "="*50)
print("TASK 2: Investor Transactions Exploration")
print("="*50)

investor_txn = pd.read_csv("C:/Users/user/mutual-fund-analytics/data/raw/08_investor_transactions.csv")
print(investor_txn.columns.tolist())
print(investor_txn.dtypes)

investor_txn = pd.read_csv("C:/Users/user/mutual-fund-analytics/data/raw/08_investor_transactions.csv")

print("Before cleaning:", investor_txn.shape)

# 1. Standardize transaction_type values
investor_txn['transaction_type'] = investor_txn['transaction_type'].str.strip().str.title()

# 2. Validate amount > 0
invalid_amount = (investor_txn['amount_inr'] <= 0).sum()
print(f"Invalid amount rows: {invalid_amount}")
investor_txn = investor_txn[investor_txn['amount_inr'] > 0]

# 3. Fix date formats
investor_txn['transaction_date'] = pd.to_datetime(investor_txn['transaction_date'], errors='coerce')

# 4. Check KYC status enum values
print("KYC status categories:")
print(investor_txn['kyc_status'].value_counts())

# Remove invalid/null dates after conversion
invalid_dates = investor_txn['transaction_date'].isna().sum()
print(f"Invalid date rows: {invalid_dates}")
investor_txn = investor_txn.dropna(subset=['transaction_date'])

print("After cleaning:", investor_txn.shape)

investor_txn.to_csv("C:/Users/user/mutual-fund-analytics/data/processed/08_investor_transactions_cleaned.csv", index=False)
print("Saved!")

print("\n" + "="*50)
print(" cleaning all datasets")
print("="*50)


import os

raw_path = "C:/Users/user/mutual-fund-analytics/data/raw/"
files = [
    "03_aum_by_fund_house", "04_monthly_sip_inflows",
    "05_category_inflows", "06_industry_folio_count", "07_scheme_performance",
    "09_portfolio_holdings", "10_benchmark_indices"
]

for f in files:
    df = pd.read_csv(raw_path + f + ".csv")
    print(f"\n{f}: {df.shape}")
    print(df.columns.tolist())

    print("\n" + "="*50)
print("CLEANING REMAINING FILES")
print("="*50)

raw_path = "C:/Users/user/mutual-fund-analytics/data/raw/"
processed_path = "C:/Users/user/mutual-fund-analytics/data/processed/"

# 03_aum_by_fund_house
df = pd.read_csv(raw_path + "03_aum_by_fund_house.csv")
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df = df.drop_duplicates()
df = df.dropna(subset=['date'])
df.to_csv(processed_path + "03_aum_by_fund_house_cleaned.csv", index=False)
print("03 done:", df.shape)

# 04_monthly_sip_inflows
df = pd.read_csv(raw_path + "04_monthly_sip_inflows.csv")
df['month'] = pd.to_datetime(df['month'], errors='coerce')
df = df.drop_duplicates()
df.to_csv(processed_path + "04_monthly_sip_inflows_cleaned.csv", index=False)
print("04 done:", df.shape)

# 05_category_inflows
df = pd.read_csv(raw_path + "05_category_inflows.csv")
df['month'] = pd.to_datetime(df['month'], errors='coerce')
df['category'] = df['category'].str.strip().str.title()
df = df.drop_duplicates()
df.to_csv(processed_path + "05_category_inflows_cleaned.csv", index=False)
print("05 done:", df.shape)

# 06_industry_folio_count
df = pd.read_csv(raw_path + "06_industry_folio_count.csv")
df['month'] = pd.to_datetime(df['month'], errors='coerce')
df = df.drop_duplicates()
df.to_csv(processed_path + "06_industry_folio_count_cleaned.csv", index=False)
print("06 done:", df.shape)

# 09_portfolio_holdings
df = pd.read_csv(raw_path + "09_portfolio_holdings.csv")
df['portfolio_date'] = pd.to_datetime(df['portfolio_date'], errors='coerce')
df = df.drop_duplicates()
df = df[df['weight_pct'] > 0]  # validate weight is positive
df.to_csv(processed_path + "09_portfolio_holdings_cleaned.csv", index=False)
print("09 done:", df.shape)

# 10_benchmark_indices
df = pd.read_csv(raw_path + "10_benchmark_indices.csv")
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df = df.drop_duplicates()
df = df[df['close_value'] > 0]
df.to_csv(processed_path + "10_benchmark_indices_cleaned.csv", index=False)
print("10 done:", df.shape)

print("\n" + "="*50)
print("TASK 3: Cleaning Scheme Performance")
print("="*50)

df = pd.read_csv(raw_path + "07_scheme_performance.csv")
print("Before cleaning:", df.shape)

# Validate return columns are numeric
return_cols = ['return_1yr_pct', 'return_3yr_pct', 'return_5yr_pct', 'benchmark_3yr_pct']
for col in return_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Flag anomalies (extreme outlier returns, e.g., beyond -100% to 200%)
for col in return_cols:
    anomalies = df[(df[col] < -100) | (df[col] > 200)]
    print(f"Anomalies in {col}: {len(anomalies)}")

# Check expense_ratio range (0.1% - 2.5%)
invalid_expense = df[(df['expense_ratio_pct'] < 0.1) | (df['expense_ratio_pct'] > 2.5)]
print(f"Invalid expense_ratio rows: {len(invalid_expense)}")

# Remove rows with NaN in critical return columns
df = df.dropna(subset=return_cols)

print("After cleaning:", df.shape)

df.to_csv(processed_path + "07_scheme_performance_cleaned.csv", index=False)
print("07 done!")

print("\n" + "="*50)
print("TASK 4: Creating SQLite Star Schema")
print("="*50)

import sqlite3

conn = sqlite3.connect("C:/Users/user/mutual-fund-analytics/bluestock_mf.db")
cursor = conn.cursor()

# dim_fund - dimension table for fund details
cursor.execute("""
CREATE TABLE IF NOT EXISTS dim_fund (
    amfi_code INTEGER PRIMARY KEY,
    fund_house TEXT,
    scheme_name TEXT,
    category TEXT,
    sub_category TEXT,
    plan TEXT,
    risk_category TEXT
)
""")

# dim_date - dimension table for dates
cursor.execute("""
CREATE TABLE IF NOT EXISTS dim_date (
    date_id TEXT PRIMARY KEY,
    full_date DATE,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    day_of_week TEXT
)
""")

# fact_nav - fact table for NAV history
cursor.execute("""
CREATE TABLE IF NOT EXISTS fact_nav (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code INTEGER,
    date TEXT,
    nav REAL,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
)
""")

# fact_transactions - fact table for investor transactions
cursor.execute("""
CREATE TABLE IF NOT EXISTS fact_transactions (
    investor_id TEXT,
    transaction_date TEXT,
    amfi_code INTEGER,
    transaction_type TEXT,
    amount_inr INTEGER,
    state TEXT,
    city TEXT,
    kyc_status TEXT,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
)
""")

# fact_performance - fact table for scheme performance
cursor.execute("""
CREATE TABLE IF NOT EXISTS fact_performance (
    amfi_code INTEGER,
    return_1yr_pct REAL,
    return_3yr_pct REAL,
    return_5yr_pct REAL,
    expense_ratio_pct REAL,
    sharpe_ratio REAL,
    risk_grade TEXT,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
)
""")

# fact_aum - fact table for AUM by fund house
cursor.execute("""
CREATE TABLE IF NOT EXISTS fact_aum (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    fund_house TEXT,
    aum_crore REAL,
    num_schemes INTEGER
)
""")

conn.commit()
print("Star schema created successfully!")
conn.close()


import sqlite3

conn = sqlite3.connect("C:/Users/user/mutual-fund-analytics/bluestock_mf.db")
cursor = conn.cursor()

# Drop old tables (from earlier attempt)
cursor.execute("DROP TABLE IF EXISTS dim_fund")
cursor.execute("DROP TABLE IF EXISTS dim_date")
cursor.execute("DROP TABLE IF EXISTS fact_nav")
cursor.execute("DROP TABLE IF EXISTS fact_transactions")
cursor.execute("DROP TABLE IF EXISTS fact_performance")
cursor.execute("DROP TABLE IF EXISTS fact_aum")
conn.commit()
print("Old tables dropped!")

# Now apply new schema from schema.sql
with open("C:/Users/user/mutual-fund-analytics/sql/schema.sql", "r") as f:
    schema_sql = f.read()

cursor.executescript(schema_sql)
conn.commit()
print("New schema applied successfully!")
conn.close()

print("\n" + "="*50)
print("TASK 5: Loading Data into SQLite")
print("="*50)

from sqlalchemy import create_engine

engine = create_engine("sqlite:///C:/Users/user/mutual-fund-analytics/bluestock_mf.db")
processed_path = "C:/Users/user/mutual-fund-analytics/data/processed/"
raw_path = "C:/Users/user/mutual-fund-analytics/data/raw/"

# Load dim_fund
fund_master = pd.read_csv(raw_path + "01_fund_master.csv")
dim_fund = fund_master[['amfi_code', 'fund_house', 'scheme_name', 'category', 'sub_category', 'plan', 'risk_category']].copy()
dim_fund['amfi_code'] = dim_fund['amfi_code'].astype(str)
dim_fund.to_sql('dim_fund', engine, if_exists='append', index=False)
print("dim_fund loaded:", len(dim_fund))

# Load fact_nav with daily_return calculated
nav_history = pd.read_csv(processed_path + "02_nav_history_cleaned.csv")
nav_history['amfi_code'] = nav_history['amfi_code'].astype(str)
nav_history = nav_history.sort_values(['amfi_code', 'date'])
nav_history['daily_return'] = nav_history.groupby('amfi_code')['nav'].pct_change() * 100
nav_history = nav_history.rename(columns={'date': 'nav_date'})
fact_nav = nav_history[['amfi_code', 'nav_date', 'nav', 'daily_return']]
fact_nav.to_sql('fact_nav', engine, if_exists='append', index=False)
print("fact_nav loaded:", len(fact_nav))

# Load fact_transactions
investor_txn = pd.read_csv(processed_path + "08_investor_transactions_cleaned.csv")
investor_txn['amfi_code'] = investor_txn['amfi_code'].astype(str)
fact_txn = investor_txn[['investor_id', 'transaction_date', 'amfi_code', 'transaction_type', 'amount_inr', 'state', 'city', 'kyc_status']]
fact_txn.to_sql('fact_transactions', engine, if_exists='append', index=False)
print("fact_transactions loaded:", len(fact_txn))

# Load fact_performance
scheme_perf = pd.read_csv(processed_path + "07_scheme_performance_cleaned.csv")
scheme_perf['amfi_code'] = scheme_perf['amfi_code'].astype(str)
fact_perf = scheme_perf[['amfi_code', 'return_1yr_pct', 'return_3yr_pct', 'return_5yr_pct', 'expense_ratio_pct', 'sharpe_ratio', 'risk_grade']]
fact_perf.to_sql('fact_performance', engine, if_exists='append', index=False)
print("fact_performance loaded:", len(fact_perf))

# Load fact_aum
aum_data = pd.read_csv(processed_path + "03_aum_by_fund_house_cleaned.csv")
fact_aum = aum_data[['date', 'fund_house', 'aum_crore', 'num_schemes']]
fact_aum.to_sql('fact_aum', engine, if_exists='append', index=False)
print("fact_aum loaded:", len(fact_aum))

print("\nAll tables loaded successfully!")


print("\n" + "="*50)
print("TASK 6: Running Analytical SQL Queries")
print("="*50)

import sqlite3
conn = sqlite3.connect("C:/Users/user/mutual-fund-analytics/bluestock_mf.db")

queries = {}

# Q1: Top 5 funds by AUM
queries['Q1_top5_funds_by_aum'] = """
SELECT fund_house, aum_crore
FROM fact_aum
ORDER BY aum_crore DESC
LIMIT 5
"""

# Q2: Average NAV per month
queries['Q2_avg_nav_per_month'] = """
SELECT strftime('%Y-%m', nav_date) as month, AVG(nav) as avg_nav
FROM fact_nav
GROUP BY month
ORDER BY month
"""

# Q3: SIP inflow YoY growth (from raw file directly since it's not in DB)
queries['Q3_sip_yoy_growth'] = "SELECT 'Run separately from 04_monthly_sip_inflows_cleaned.csv - yoy_growth_pct column' as note"

# Q4: Transactions by state
queries['Q4_transactions_by_state'] = """
SELECT state, COUNT(*) as total_transactions, SUM(amount_inr) as total_amount
FROM fact_transactions
GROUP BY state
ORDER BY total_transactions DESC
"""

# Q5: Funds with expense_ratio < 1%
queries['Q5_low_expense_funds'] = """
SELECT f.scheme_name, f.fund_house, p.expense_ratio_pct
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
WHERE p.expense_ratio_pct < 1
ORDER BY p.expense_ratio_pct
"""

# Q6: Top 5 funds by 1-year return
queries['Q6_top5_by_1yr_return'] = """
SELECT f.scheme_name, p.return_1yr_pct
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
ORDER BY p.return_1yr_pct DESC
LIMIT 5
"""

# Q7: Transaction type distribution
queries['Q7_transaction_type_distribution'] = """
SELECT transaction_type, COUNT(*) as count, SUM(amount_inr) as total_amount
FROM fact_transactions
GROUP BY transaction_type
"""

# Q8: KYC status breakdown
queries['Q8_kyc_status_breakdown'] = """
SELECT kyc_status, COUNT(*) as investor_count
FROM fact_transactions
GROUP BY kyc_status
"""

# Q9: Average expense ratio by category
queries['Q9_avg_expense_by_category'] = """
SELECT f.category, AVG(p.expense_ratio_pct) as avg_expense_ratio
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
GROUP BY f.category
"""

# Q10: Funds by risk grade count
queries['Q10_funds_by_risk_grade'] = """
SELECT risk_grade, COUNT(*) as fund_count
FROM fact_performance
GROUP BY risk_grade
"""

# Run all queries and save results
results_text = ""
for name, query in queries.items():
    print(f"\n--- {name} ---")
    try:
        result = pd.read_sql(query, conn)
        print(result)
        results_text += f"\n-- {name} --\n{query}\n\nResults:\n{result.to_string()}\n\n"
    except Exception as e:
        print(f"Error: {e}")

conn.close()

# Save queries.sql file
with open("C:/Users/user/mutual-fund-analytics/sql/queries.sql", "w") as f:
    for name, query in queries.items():
        f.write(f"-- {name}\n{query}\n\n")

print("\nqueries.sql saved!")