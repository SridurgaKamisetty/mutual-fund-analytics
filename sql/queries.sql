-- Q1_top5_funds_by_aum

SELECT fund_house, aum_crore
FROM fact_aum
ORDER BY aum_crore DESC
LIMIT 5


-- Q2_avg_nav_per_month

SELECT strftime('%Y-%m', nav_date) as month, AVG(nav) as avg_nav
FROM fact_nav
GROUP BY month
ORDER BY month


-- Q3_sip_yoy_growth
SELECT 'Run separately from 04_monthly_sip_inflows_cleaned.csv - yoy_growth_pct column' as note

-- Q4_transactions_by_state

SELECT state, COUNT(*) as total_transactions, SUM(amount_inr) as total_amount
FROM fact_transactions
GROUP BY state
ORDER BY total_transactions DESC


-- Q5_low_expense_funds

SELECT f.scheme_name, f.fund_house, p.expense_ratio_pct
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
WHERE p.expense_ratio_pct < 1
ORDER BY p.expense_ratio_pct


-- Q6_top5_by_1yr_return

SELECT f.scheme_name, p.return_1yr_pct
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
ORDER BY p.return_1yr_pct DESC
LIMIT 5


-- Q7_transaction_type_distribution

SELECT transaction_type, COUNT(*) as count, SUM(amount_inr) as total_amount
FROM fact_transactions
GROUP BY transaction_type


-- Q8_kyc_status_breakdown

SELECT kyc_status, COUNT(*) as investor_count
FROM fact_transactions
GROUP BY kyc_status


-- Q9_avg_expense_by_category

SELECT f.category, AVG(p.expense_ratio_pct) as avg_expense_ratio
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
GROUP BY f.category


-- Q10_funds_by_risk_grade

SELECT risk_grade, COUNT(*) as fund_count
FROM fact_performance
GROUP BY risk_grade


