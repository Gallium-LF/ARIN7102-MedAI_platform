import csv
import json

input_file = "backend/data/customer_purchase_data.csv"
output_ts_file = "kpiData.ts"

with open(input_file, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

total_users = len(rows)
purchase_count = sum(1 for r in rows if r["PurchaseStatus"].strip() == "1")
loyalty_count = sum(1 for r in rows if r["LoyaltyProgram"].strip() == "1")

total_time = sum(float(r["TimeSpentOnWebsite"]) for r in rows)
total_discount = sum(float(r["DiscountsAvailed"]) for r in rows)

avg_time = total_time / total_users if total_users else 0
avg_discount = total_discount / total_users if total_users else 0
purchase_rate = purchase_count / total_users if total_users else 0
loyalty_rate = loyalty_count / total_users if total_users else 0

# TypeScript 数据文件写入
with open(output_ts_file, "w", encoding="utf-8") as f:
    f.write("export const kpiData = {\n")
    f.write(f"  totalUsers: {total_users},\n")
    f.write(f"  purchaseRate: {round(purchase_rate, 4)},\n")
    f.write(f"  avgTime: {round(avg_time, 2)},\n")
    f.write(f"  loyaltyRate: {round(loyalty_rate, 4)},\n")
    f.write(f"  avgDiscounts: {round(avg_discount, 2)}\n")
    f.write("};\n")

print("✅ KPI 数据已写入 kpiData.ts")
