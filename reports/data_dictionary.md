# Data Dictionary — Mutual Fund Analytics

## dim_fund
| Column | Type | Description |
|---|---|---|
| amfi_code | TEXT (PK) | Unique identifier for each mutual fund scheme, assigned by AMFI |
| fund_house | TEXT | Asset Management Company (AMC) managing the fund |
| scheme_name | TEXT | Official name of the mutual fund scheme |
| category | TEXT | Broad fund category (e.g., Equity, Debt, Hybrid) |
| sub_category | TEXT | Specific sub-type within category (e.g., Large Cap, Mid Cap) |
| plan | TEXT | Plan type (Direct/Regular) |
| risk_category | TEXT | Risk level classification (Low/Moderate/High) |

## fact_nav
| Column | Type | Description |
|---|---|---|
| amfi_code | TEXT (FK) | Links to dim_fund |
| nav_date | DATE | Date of NAV record |
| nav | REAL | Net Asset Value per unit on that date |
| daily_return | REAL | Percentage change in NAV from previous day |

## fact_transactions
| Column | Type | Description |
|---|---|---|
| investor_id | TEXT | Unique investor identifier |
| transaction_date | DATE | Date transaction occurred |
| amfi_code | TEXT (FK) | Fund involved in transaction |
| transaction_type | TEXT | SIP / Lumpsum / Redemption |
| amount_inr | INTEGER | Transaction amount in INR |
| state | TEXT | Investor's state |
| city | TEXT | Investor's city |
| kyc_status | TEXT | KYC verification status |

## fact_performance
| Column | Type | Description |
|---|---|---|
| amfi_code | TEXT (FK) | Fund identifier |
| return_1yr_pct | REAL | 1-year trailing return (%) |
| return_3yr_pct | REAL | 3-year trailing return (%) |
| return_5yr_pct | REAL | 5-year trailing return (%) |
| expense_ratio_pct | REAL | Annual fee charged by fund (0.1%-2.5% range) |
| sharpe_ratio | REAL | Risk-adjusted return measure |
| risk_grade | TEXT | Risk classification grade |

## fact_aum
| Column | Type | Description |
|---|---|---|
| date | DATE | Reporting date |
| fund_house | TEXT | Asset Management Company |
| aum_crore | REAL | Assets Under Management (in Crores INR) |
| num_schemes | INTEGER | Number of schemes offered by that fund house |

## Data Quality Notes
- nav_history: Forward-filled for weekends/holidays (46,000 → 64,320 rows after gap-filling)
- scheme_performance: 0 anomalies found in return values; expense ratios all within valid 0.1%-2.5% range
- investor_transactions: No invalid amounts or dates found in source data
- Source: All data provided by Bluestock Fintech for Mutual Fund Analytics Capstone Project