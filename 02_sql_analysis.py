"""
================================================
SWIGGY SALES DATA ANALYSIS
Tool: SQL (SQLite via Python)
================================================
"""

import sqlite3
import pandas as pd

# ── Setup DB ──────────────────────────────────────────────────
conn = sqlite3.connect('../data/swiggy.db')
df = pd.read_csv('../data/swiggy_orders.csv')
df.to_sql('orders', conn, if_exists='replace', index=False)
print("=" * 60)
print("   SWIGGY SALES — SQL ANALYSIS (SQLite)")
print("=" * 60)

def run_sql(title, query):
    print(f"\n{'─'*60}")
    print(f"  {title}")
    print(f"{'─'*60}")
    result = pd.read_sql_query(query, conn)
    print(result.to_string(index=False))
    return result

# ── Q1: Overall KPIs ──────────────────────────────────────────
run_sql("QUERY 1: Overall KPIs", """
SELECT
    COUNT(*) AS total_orders,
    SUM(CASE WHEN order_status='Delivered' THEN 1 ELSE 0 END) AS delivered,
    ROUND(AVG(CASE WHEN order_status='Delivered' THEN final_amount END), 2) AS avg_order_value,
    ROUND(SUM(CASE WHEN order_status='Delivered' THEN final_amount END), 2) AS total_revenue,
    ROUND(SUM(discount_amount), 2) AS total_discount_given,
    ROUND(AVG(delivery_time_mins), 1) AS avg_delivery_mins,
    ROUND(AVG(customer_rating), 2) AS avg_rating
FROM orders
""")

# ── Q2: City Revenue Ranking ──────────────────────────────────
run_sql("QUERY 2: City Revenue Ranking with RANK()", """
SELECT
    city,
    COUNT(*) AS total_orders,
    ROUND(SUM(final_amount), 2) AS total_revenue,
    ROUND(AVG(final_amount), 2) AS avg_order_value,
    ROUND(AVG(customer_rating), 2) AS avg_rating,
    RANK() OVER (ORDER BY SUM(final_amount) DESC) AS revenue_rank
FROM orders
WHERE order_status = 'Delivered'
GROUP BY city
ORDER BY revenue_rank
""")

# ── Q3: Monthly Revenue with Growth ───────────────────────────
run_sql("QUERY 3: Monthly Revenue with MoM Growth %", """
WITH monthly AS (
    SELECT
        year, month,
        ROUND(SUM(final_amount), 2) AS revenue
    FROM orders
    WHERE order_status = 'Delivered'
    GROUP BY year, month
),
with_lag AS (
    SELECT *,
        LAG(revenue) OVER (ORDER BY year, month) AS prev_revenue
    FROM monthly
)
SELECT
    year,
    month,
    revenue,
    prev_revenue,
    CASE
        WHEN prev_revenue IS NULL THEN NULL
        ELSE ROUND((revenue - prev_revenue) * 100.0 / prev_revenue, 1)
    END AS mom_growth_pct
FROM with_lag
ORDER BY year, month
""")

# ── Q4: Top 5 Restaurants per City ────────────────────────────
run_sql("QUERY 4: Top 3 Restaurants per City (Window Function)", """
WITH ranked AS (
    SELECT
        city,
        restaurant_name,
        COUNT(*) AS orders,
        ROUND(SUM(final_amount), 2) AS revenue,
        ROUND(AVG(customer_rating), 2) AS avg_rating,
        ROW_NUMBER() OVER (PARTITION BY city ORDER BY SUM(final_amount) DESC) AS rn
    FROM orders
    WHERE order_status = 'Delivered'
    GROUP BY city, restaurant_name
)
SELECT city, restaurant_name, orders, revenue, avg_rating
FROM ranked
WHERE rn <= 3
ORDER BY city, rn
""")

# ── Q5: Cuisine Performance ───────────────────────────────────
run_sql("QUERY 5: Cuisine Performance Analysis", """
SELECT
    cuisine_type,
    COUNT(*) AS orders,
    ROUND(SUM(final_amount), 2) AS revenue,
    ROUND(AVG(final_amount), 2) AS avg_revenue,
    ROUND(AVG(discount_amount), 2) AS avg_discount,
    ROUND(AVG(customer_rating), 2) AS avg_rating,
    ROUND(SUM(final_amount) * 100.0 / SUM(SUM(final_amount)) OVER(), 2) AS revenue_share_pct
FROM orders
WHERE order_status = 'Delivered'
GROUP BY cuisine_type
ORDER BY revenue DESC
""")

# ── Q6: Payment Method Analysis ───────────────────────────────
run_sql("QUERY 6: Payment Method Analysis", """
SELECT
    payment_method,
    COUNT(*) AS orders,
    ROUND(SUM(final_amount), 2) AS revenue,
    ROUND(AVG(final_amount), 2) AS avg_order_value,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1) AS order_share_pct
FROM orders
GROUP BY payment_method
ORDER BY orders DESC
""")

# ── Q7: Customer Segmentation ─────────────────────────────────
run_sql("QUERY 7: Customer Segmentation by Order Frequency", """
WITH customer_orders AS (
    SELECT
        customer_id,
        COUNT(*) AS order_count,
        ROUND(SUM(final_amount), 2) AS lifetime_value,
        ROUND(AVG(final_amount), 2) AS avg_order_value,
        ROUND(AVG(customer_rating), 2) AS avg_rating
    FROM orders
    WHERE order_status = 'Delivered'
    GROUP BY customer_id
),
segmented AS (
    SELECT *,
        CASE
            WHEN order_count >= 5 THEN 'VIP (5+ orders)'
            WHEN order_count >= 3 THEN 'Regular (3-4)'
            ELSE 'Occasional (1-2)'
        END AS segment
    FROM customer_orders
)
SELECT
    segment,
    COUNT(*) AS customers,
    ROUND(AVG(order_count), 1) AS avg_orders,
    ROUND(AVG(lifetime_value), 2) AS avg_lifetime_value,
    ROUND(SUM(lifetime_value), 2) AS total_revenue
FROM segmented
GROUP BY segment
ORDER BY avg_orders DESC
""")

# ── Q8: Peak Hours by Day Type ────────────────────────────────
run_sql("QUERY 8: Top 5 Peak Hours (Weekday vs Weekend)", """
WITH hour_stats AS (
    SELECT
        hour_of_day,
        is_weekend,
        COUNT(*) AS orders,
        ROUND(AVG(final_amount), 2) AS avg_order_value,
        ROW_NUMBER() OVER (PARTITION BY is_weekend ORDER BY COUNT(*) DESC) AS rn
    FROM orders
    WHERE order_status = 'Delivered'
    GROUP BY hour_of_day, is_weekend
)
SELECT
    CASE WHEN is_weekend = 0 THEN 'Weekday' ELSE 'Weekend' END AS day_type,
    hour_of_day || ':00' AS hour,
    orders,
    avg_order_value
FROM hour_stats
WHERE rn <= 5
ORDER BY is_weekend, rn
""")

# ── Q9: Quarterly Revenue ─────────────────────────────────────
run_sql("QUERY 9: Quarterly Revenue by Year", """
SELECT
    year,
    'Q' || quarter AS quarter,
    COUNT(*) AS orders,
    ROUND(SUM(final_amount), 2) AS revenue,
    ROUND(AVG(final_amount), 2) AS avg_order_value
FROM orders
WHERE order_status = 'Delivered'
GROUP BY year, quarter
ORDER BY year, quarter
""")

# ── Q10: High Value Customers ─────────────────────────────────
run_sql("QUERY 10: Top 10 Customers by Lifetime Value", """
SELECT
    customer_id,
    COUNT(*) AS total_orders,
    ROUND(SUM(final_amount), 2) AS lifetime_value,
    ROUND(AVG(final_amount), 2) AS avg_order_value,
    ROUND(AVG(customer_rating), 2) AS avg_rating,
    MAX(city) AS primary_city
FROM orders
WHERE order_status = 'Delivered'
GROUP BY customer_id
ORDER BY lifetime_value DESC
LIMIT 10
""")

conn.close()
print("\n" + "=" * 60)
print("  SQL Analysis Complete!")
print("=" * 60)
