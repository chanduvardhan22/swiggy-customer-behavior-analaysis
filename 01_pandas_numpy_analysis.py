"""
================================================
SWIGGY SALES DATA ANALYSIS
Tool: Pandas + NumPy
================================================
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("   SWIGGY SALES DATA ANALYSIS — Pandas & NumPy")
print("=" * 60)

# ── Load Data ──────────────────────────────────────────────────
df = pd.read_csv('../data/swiggy_orders.csv', parse_dates=['order_date'])

# ── 1. DATA OVERVIEW ──────────────────────────────────────────
print("\n[1] DATASET OVERVIEW")
print(f"  Shape        : {df.shape}")
print(f"  Date Range   : {df['order_date'].min().date()} → {df['order_date'].max().date()}")
print(f"  Columns      : {list(df.columns)}")
print(f"\n  Dtypes:\n{df.dtypes.to_string()}")
print(f"\n  Missing Values:\n{df.isnull().sum()[df.isnull().sum() > 0].to_string() or '  None'}")

# ── 2. DESCRIPTIVE STATISTICS (NumPy) ─────────────────────────
print("\n[2] DESCRIPTIVE STATISTICS (NumPy)")
numeric_cols = ['order_value', 'final_amount', 'discount_amount', 'delivery_time_mins', 'customer_rating']
for col in numeric_cols:
    arr = df[col].values
    print(f"\n  {col}:")
    print(f"    Mean   = ₹{np.mean(arr):.2f}" if 'amount' in col or 'value' in col else f"    Mean   = {np.mean(arr):.2f}")
    print(f"    Median = {np.median(arr):.2f}")
    print(f"    Std    = {np.std(arr):.2f}")
    print(f"    Min    = {np.min(arr):.2f}  |  Max = {np.max(arr):.2f}")
    print(f"    P25    = {np.percentile(arr, 25):.2f}  |  P75 = {np.percentile(arr, 75):.2f}")

# ── 3. SALES KPIs ──────────────────────────────────────────────
print("\n[3] KEY PERFORMANCE INDICATORS")
delivered = df[df['order_status'] == 'Delivered']
print(f"  Total Orders      : {len(df):,}")
print(f"  Delivered Orders  : {len(delivered):,} ({len(delivered)/len(df)*100:.1f}%)")
print(f"  Cancellation Rate : {(df['order_status']=='Cancelled').mean()*100:.1f}%")
print(f"  Total Revenue     : ₹{delivered['final_amount'].sum():,.2f}")
print(f"  Avg Order Value   : ₹{delivered['final_amount'].mean():.2f}")
print(f"  Total Discount    : ₹{df['discount_amount'].sum():,.2f}")
print(f"  Avg Delivery Time : {df['delivery_time_mins'].mean():.1f} mins")
print(f"  Avg Rating        : {df['customer_rating'].mean():.2f} / 5.0")

# ── 4. CITY-WISE ANALYSIS ─────────────────────────────────────
print("\n[4] CITY-WISE REVENUE (Delivered Orders)")
city_stats = delivered.groupby('city').agg(
    Total_Revenue=('final_amount', 'sum'),
    Total_Orders=('order_id', 'count'),
    Avg_Order_Value=('final_amount', 'mean'),
    Avg_Rating=('customer_rating', 'mean')
).sort_values('Total_Revenue', ascending=False)
city_stats['Revenue_Share%'] = (city_stats['Total_Revenue'] / city_stats['Total_Revenue'].sum() * 100).round(1)
print(city_stats.round(2).to_string())

# ── 5. CUISINE-WISE ANALYSIS ──────────────────────────────────
print("\n[5] TOP CUISINES BY ORDER COUNT")
cuisine_stats = delivered.groupby('cuisine_type').agg(
    Orders=('order_id', 'count'),
    Revenue=('final_amount', 'sum'),
    Avg_Rating=('customer_rating', 'mean')
).sort_values('Orders', ascending=False).head(8)
print(cuisine_stats.round(2).to_string())

# ── 6. MONTHLY TREND ──────────────────────────────────────────
print("\n[6] MONTHLY REVENUE TREND")
monthly = delivered.groupby(['year', 'month'])['final_amount'].sum().reset_index()
monthly['YearMonth'] = monthly['year'].astype(str) + '-' + monthly['month'].astype(str).str.zfill(2)
print(monthly[['YearMonth', 'final_amount']].rename(columns={'final_amount': 'Revenue'}).to_string(index=False))

# ── 7. PAYMENT METHOD ANALYSIS ────────────────────────────────
print("\n[7] PAYMENT METHOD BREAKDOWN")
payment_stats = df.groupby('payment_method').agg(
    Orders=('order_id', 'count'),
    Revenue=('final_amount', 'sum')
).sort_values('Orders', ascending=False)
payment_stats['Order_Share%'] = (payment_stats['Orders'] / payment_stats['Orders'].sum() * 100).round(1)
print(payment_stats.round(2).to_string())

# ── 8. PEAK HOURS ─────────────────────────────────────────────
print("\n[8] PEAK ORDERING HOURS")
hour_stats = delivered.groupby('hour_of_day')['order_id'].count().reset_index()
hour_stats.columns = ['Hour', 'Orders']
hour_stats['Bar'] = hour_stats['Orders'].apply(lambda x: '█' * (x // 20))
print(hour_stats.to_string(index=False))

# ── 9. WEEKEND VS WEEKDAY ─────────────────────────────────────
print("\n[9] WEEKEND vs WEEKDAY")
wk = delivered.groupby('is_weekend').agg(
    Orders=('order_id', 'count'),
    Revenue=('final_amount', 'sum'),
    Avg_Order_Value=('final_amount', 'mean')
)
wk.index = ['Weekday', 'Weekend']
print(wk.round(2).to_string())

# ── 10. CORRELATION MATRIX (NumPy) ────────────────────────────
print("\n[10] CORRELATION MATRIX (NumPy)")
cols = ['order_value', 'discount_amount', 'delivery_fee', 'final_amount', 'delivery_time_mins', 'customer_rating']
corr_matrix = np.corrcoef(df[cols].values.T)
corr_df = pd.DataFrame(corr_matrix, index=cols, columns=cols)
print(corr_df.round(3).to_string())

# ── 11. ADVANCED NUMPY STATS ──────────────────────────────────
print("\n[11] ADVANCED NUMPY ANALYSIS")
revenue_arr = delivered['final_amount'].values
print(f"  Revenue Variance       : {np.var(revenue_arr):.2f}")
print(f"  Revenue Skewness (approx): {(np.mean(revenue_arr) - np.median(revenue_arr)) / np.std(revenue_arr):.3f}")
bins = np.linspace(revenue_arr.min(), revenue_arr.max(), 6)
hist, edges = np.histogram(revenue_arr, bins=bins)
print(f"\n  Revenue Distribution (histogram):")
for i, count in enumerate(hist):
    print(f"    ₹{edges[i]:.0f}–₹{edges[i+1]:.0f}: {count} orders  {'█' * (count // 30)}")

# ── 12. TOP 10 RESTAURANTS ────────────────────────────────────
print("\n[12] TOP 10 RESTAURANTS BY REVENUE")
top_restaurants = delivered.groupby('restaurant_name').agg(
    Revenue=('final_amount', 'sum'),
    Orders=('order_id', 'count'),
    Avg_Rating=('customer_rating', 'mean')
).sort_values('Revenue', ascending=False).head(10)
print(top_restaurants.round(2).to_string())

print("\n" + "=" * 60)
print("  Analysis Complete! Saving results...")
print("=" * 60)

# Save all summary tables to CSV
city_stats.to_csv('../data/city_summary.csv')
cuisine_stats.to_csv('../data/cuisine_summary.csv')
monthly.to_csv('../data/monthly_trend.csv', index=False)
payment_stats.to_csv('../data/payment_summary.csv')
top_restaurants.to_csv('../data/top_restaurants.csv')

print("  Saved: city_summary, cuisine_summary, monthly_trend, payment_summary, top_restaurants")
