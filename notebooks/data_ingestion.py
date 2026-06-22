import pandas as pandas
import os
files=[
    "01_fund_master",
    "02_nav_history",
    "03_aum_by_fund_house",
    "04_monthly_sip_inflows",
    "05_category_inflows",
    "06_industry_folio_count",
    "07_scheme_performance",
    "08_investor_transactions",
    "09_portfolio_holdings",
    "10_benchmark_indices"
    ]
path="C:/Users/user/mutual-fund-analytics/data/raw/"
for file in files:
    df=pandas.read_csv (path + file + ".csv")
    print(f"/n{'='*50}")
    print(f"File: {file}")
    print(f"shape: {df.shape}")
    print(f"head:/n {df.head()}")
    print(f"dtypes:/n {df.dtypes}")