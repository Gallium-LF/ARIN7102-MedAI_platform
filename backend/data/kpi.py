import pandas as pd

csv_path = "backend/data/train.csv"

df = pd.read_csv(csv_path)

df_open = df[df["Open"] == 1]

total_sales = df_open["Sales"].sum()

total_customers = df_open["Customers"].sum()

unique_stores = df["Store"].nunique()
avg_sales_per_store = total_sales / unique_stores if unique_stores else 0

promo_sales = df_open[df_open["Promo"] == 1]["Sales"]
promo_avg_sales = promo_sales.mean()

open_holiday_stores = df[(df["Open"] == 1) & (df["StateHoliday"].astype(str) != "0")][
    "Store"
].nunique()

print("✅ Total Sales:", int(total_sales))
print("✅ Total Customers:", int(total_customers))
print("✅ Average Sales per Store:", round(avg_sales_per_store, 2))
print("✅ Promo Day Avg Sales:", round(promo_avg_sales, 2))
print("✅ Open Store Count on State Holidays:", int(open_holiday_stores))
