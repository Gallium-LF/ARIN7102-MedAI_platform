import csv
from datetime import datetime

input_file = "backend/data/merged_file.csv"
output_ts_file = "reviewData.ts"
MAX_ITEMS = 1000  # 限制输出数量

month_str_to_num = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12,
}


def extract_month(date_str):
    try:
        # 日期格式如 "29-Sep-17"
        parts = date_str.strip().split("-")
        if len(parts) >= 2:
            return month_str_to_num.get(parts[1], 0)
    except Exception:
        pass
    return 0


# 读取并排序
with open(input_file, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    reviews = list(reader)

    for r in reviews:
        r["rating"] = int(r["rating"]) if r["rating"] else 0
        r["uniqueID"] = int(r["uniqueID"]) if r["uniqueID"] else -1
        r["usefulCount"] = int(r["usefulCount"]) if r["usefulCount"] else 0
        r["month"] = extract_month(r["date"])

    # 按月份排序：12 → 1（忽略年份）
    reviews.sort(key=lambda x: x["month"], reverse=True)

# 只保留前 MAX_ITEMS 条
top_reviews = reviews[:MAX_ITEMS]

# 写入 TypeScript 文件
with open(output_ts_file, "w", encoding="utf-8") as f:
    f.write("export const reviewList = [\n")
    for r in top_reviews:
        f.write("  {\n")
        f.write(f"    uniqueID: {r['uniqueID']},\n")
        f.write(f"    drugName: \"{r['drugName']}\",\n")
        f.write(f"    condition: \"{r['condition']}\",\n")
        f.write(f"    review: `{r['review']}`,\n")
        f.write(f"    rating: {r['rating']},\n")
        f.write(f"    date: \"{r['date']}\",\n")
        f.write(f"    usefulCount: {r['usefulCount']},\n")
        f.write("  },\n")
    f.write("];\n")

print(
    f"✅ Sorted by month (ignoring year) and exported top {MAX_ITEMS} reviews to {output_ts_file}"
)
