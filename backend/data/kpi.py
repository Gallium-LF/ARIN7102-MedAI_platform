import pandas as pd

# ✅ 修改为你本地的 CSV 文件路径
csv_path = "backend/data/train.csv"  # ← 改成你自己的文件名

# 读取数据
df = pd.read_csv(csv_path)

# 只保留开店记录
df_open = df[df["Open"] == 1]

# 1. 总销售额
total_sales = df_open["Sales"].sum()

# 2. 总顾客数
total_customers = df_open["Customers"].sum()

# 3. 门店平均销售额
unique_stores = df["Store"].nunique()
avg_sales_per_store = total_sales / unique_stores if unique_stores else 0

# 4. 促销日平均销售额
promo_sales = df_open[df_open["Promo"] == 1]["Sales"]
promo_avg_sales = promo_sales.mean()

# 5. 节假日仍营业的门店数（StateHoliday ≠ 0 且 Open = 1）
open_holiday_stores = df[(df["Open"] == 1) & (df["StateHoliday"].astype(str) != "0")][
    "Store"
].nunique()

# 输出结果
print("✅ Total Sales:", int(total_sales))
print("✅ Total Customers:", int(total_customers))
print("✅ Average Sales per Store:", round(avg_sales_per_store, 2))
print("✅ Promo Day Avg Sales:", round(promo_avg_sales, 2))
print("✅ Open Store Count on State Holidays:", int(open_holiday_stores))
