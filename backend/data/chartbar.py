import csv
import json
from datetime import datetime
from collections import defaultdict

# 假设文件只包含一年内的数据
input_file = "backend/data/merged_file.csv"
output_file = "chartData.ts"

# 月份映射
month_names = [
    "jan",
    "feb",
    "mar",
    "apr",
    "may",
    "jun",
    "jul",
    "aug",
    "sep",
    "oct",
    "nov",
    "dec",
]

# 初始化月度计数器
month_counts = defaultdict(int)

# 可选：统计 usefulCount（设为 False 即只统计评论条数）
USE_USEFUL_COUNT = False

with open(input_file, newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        date_str = row["date"].strip()
        try:
            date_obj = datetime.strptime(date_str, "%d-%b-%y")
            month_idx = date_obj.month - 1
            if USE_USEFUL_COUNT:
                month_counts[month_idx] += int(row.get("usefulCount", 0))
            else:
                month_counts[month_idx] += 1
        except Exception:
            continue

# 设置活跃起始月份（如7月）
ACTIVE_START_MONTH = 6  # 0-based index (July)

# 构造 chartData 数组
chart_data = []
for i in range(12):
    chart_data.append(
        {
            "month": month_names[i],
            "height": month_counts[i],
            "active": i >= ACTIVE_START_MONTH,
        }
    )

# 写入 TS 文件
with open(output_file, "w", encoding="utf-8") as f:
    f.write("export const chartData = ")
    f.write(json.dumps(chart_data, indent=2))
    f.write(";\n")

print(f"✅ 已生成 chartData.ts，可直接用于前端")
