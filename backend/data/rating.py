import csv
import json
import random
from collections import defaultdict

# 输入输出文件
input_file = "backend/data/merged_file.csv"
output_file = "./drugData.ts"

# 数据容器
rating_map = defaultdict(list)
condition_map = {}

with open(input_file, newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        drug = row["drugName"].strip()
        condition = row["condition"].strip()

        try:
            rating = float(row["rating"])
        except ValueError:
            continue

        if not drug:
            continue

        rating_map[drug].append(rating)
        if drug not in condition_map:
            condition_map[drug] = condition

# 构建前端数据对象
drug_data = {}

# 构建前端数据对象（按字母顺序排序）
drug_data = {}

for drug in sorted(rating_map.keys()):
    ratings = rating_map[drug]
    avg_rating = round(sum(ratings) / (len(ratings) * 2), 1)
    change = round(random.uniform(-0.5, 0.5), 1)
    if change > 0:
        change = "+" + str(change)
    else:
        change = str(change)
    drug_data[drug] = {
        "rating": avg_rating,
        "change": change,
        "disease": condition_map[drug],
    }


# 转为 TS 格式字符串
ts_content = "export const drugData = " + json.dumps(drug_data, indent=2) + ";\n"

# 保存
with open(output_file, "w", encoding="utf-8") as f:
    f.write(ts_content)

print(f"✅ 转换完成，已输出到 {output_file}")
