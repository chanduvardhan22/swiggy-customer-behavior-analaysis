# 🍊 Swiggy Sales Data Analysis Project

## 📌 Project Overview
A full-stack data analysis project on Swiggy food delivery sales using **Pandas**, **NumPy**, **SQL (SQLite)**, and **Power BI-ready Excel exports**. The dataset covers 5,000 orders across 8 Indian cities over 2023–2024.

---

## 📁 Project Structure

```
swiggy_analysis/
├── data/
│   ├── generate_data.py          # Dataset generator (5000 orders)
│   ├── swiggy_orders.csv         # Main dataset
│   ├── swiggy.db                 # SQLite database
│   ├── city_summary.csv
│   ├── cuisine_summary.csv
│   ├── monthly_trend.csv
│   ├── payment_summary.csv
│   └── top_restaurants.csv
│
├── notebooks/
│   └── 01_pandas_numpy_analysis.py   # Full EDA with Pandas + NumPy
│
├── sql/
│   └── 02_sql_analysis.py            # 10 SQL queries (window functions, CTEs)
│
└── powerbi_export/
    ├── 03_powerbi_export.py          # Excel export script
    └── Swiggy_Sales_PowerBI.xlsx     # Multi-sheet formatted Excel
```

---

## 🛠️ Technologies Used

| Technology | Usage |
|---|---|
| **Python / Pandas** | Data loading, cleaning, EDA, aggregations |
| **NumPy** | Statistical computations, correlation matrix, histograms |
| **SQL (SQLite)** | CTEs, window functions, segmentation queries |
| **openpyxl** | Formatted Excel workbook creation |
| **Power BI** | Dashboard visualization (connect to Excel file) |

---

## 📊 Dataset Schema

| Column | Type | Description |
|---|---|---|
| order_id | str | Unique order identifier |
| customer_id | str | Customer identifier |
| order_date | datetime | Timestamp of order |
| city | str | City (8 Indian cities) |
| restaurant_name | str | Restaurant name |
| cuisine_type | str | Food category |
| quantity | int | Number of items |
| unit_price | float | Price per item |
| order_value | float | Pre-discount total |
| discount_amount | float | Discount applied |
| delivery_fee | float | Delivery charge |
| final_amount | float | Amount paid |
| delivery_time_mins | int | Delivery duration |
| customer_rating | float | Rating (2.5–5.0) |
| order_status | str | Delivered / Cancelled |
| payment_method | str | UPI / Card / COD / Swiggy Money |
| is_weekend | int | 0=Weekday, 1=Weekend |
| month / quarter / year | int | Time dimensions |
| hour_of_day | int | Order hour |

---

## 📈 Key Findings

### 💰 Revenue KPIs
- **Total Revenue**: ₹42,19,513 across 4,024 delivered orders
- **Avg Order Value**: ₹1,048.59
- **Cancellation Rate**: 19.5%
- **Total Discounts Given**: ₹7,42,817

### 🏙️ City Performance
1. Mumbai — ₹5,62,816 (13.3% share)
2. Kolkata — ₹5,45,606 (12.9%)
3. Ahmedabad — ₹5,36,004 (12.7%)

### 🍽️ Top Cuisines
- Burgers and Healthy food lead in revenue
- South Indian has the lowest average order value

### ⏰ Peak Hours
- **2 PM – 4 PM** is the busiest window
- Weekday orders dominate (2883 vs 1141 on weekends)

### 👥 Customer Segments
| Segment | Customers | Avg LTV |
|---|---|---|
| VIP (5+ orders) | 107 | ₹5,743 |
| Regular (3-4) | 533 | ₹3,487 |
| Occasional (1-2) | 1,121 | ₹1,558 |

### 💳 Payment Methods
- Cash on Delivery is most popular (20.9%)
- Debit Card has the highest average order value (₹1,092)

---

## 🔌 Power BI Setup Guide

### Step 1: Connect Data
1. Open Power BI Desktop
2. **Get Data** → **Excel Workbook**
3. Select `Swiggy_Sales_PowerBI.xlsx`
4. Load all 9 sheets

### Step 2: Recommended Visuals

| Visual | Sheet | Fields |
|---|---|---|
| KPI Cards | KPI_Summary | Total Revenue, Orders, Avg Rating |
| Bar Chart | City_Analysis | City vs Total_Revenue |
| Line Chart | Monthly_Trend | YearMonth vs Revenue |
| Donut Chart | Payment_Methods | payment_method vs Orders |
| Column Chart | Cuisine_Analysis | cuisine_type vs Revenue |
| Matrix Table | Restaurant_Performance | restaurant_name, city, Revenue |
| Scatter Plot | Customer_Segments | Orders vs Lifetime_Value |
| Heatmap | Hourly_Pattern | hour_of_day, Day_Type, Orders |

### Step 3: Slicers to Add
- Year slicer (2023 / 2024)
- City slicer
- Cuisine type slicer
- Order Status filter

### Step 4: DAX Measures (create in Power BI)
```dax
Total Revenue = SUM(Raw_Data[final_amount])
Avg Order Value = AVERAGE(Raw_Data[final_amount])
Delivery Rate % = DIVIDE(COUNTROWS(FILTER(Raw_Data, Raw_Data[order_status]="Delivered")), COUNTROWS(Raw_Data)) * 100
MoM Growth = 
    VAR CurrentRevenue = [Total Revenue]
    VAR PrevRevenue = CALCULATE([Total Revenue], DATEADD(Monthly_Trend[order_date], -1, MONTH))
    RETURN DIVIDE(CurrentRevenue - PrevRevenue, PrevRevenue) * 100
```

---

## 🚀 How to Run

```bash
# 1. Generate data
cd data && python generate_data.py

# 2. Run Pandas + NumPy analysis
cd ../notebooks && python 01_pandas_numpy_analysis.py

# 3. Run SQL analysis
cd ../sql && python 02_sql_analysis.py

# 4. Generate Power BI Excel
cd ../powerbi_export && python 03_powerbi_export.py

# 5. Open Swiggy_Sales_PowerBI.xlsx in Power BI Desktop
```

---

## 📦 Requirements
```
pandas
numpy
openpyxl
sqlite3 (built-in)
matplotlib (optional for charts)
seaborn (optional)
```

---

*Dataset is synthetic and generated for educational purposes.*
