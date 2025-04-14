import pandas as pd

# 替换为你真实的 CSV 路径
csv_path = "backend/data/train.csv"

# 读取销售数据
df = pd.read_csv(csv_path)

# 只保留营业数据
df = df[df["Open"] == 1]

# 提取年份（确保 Date 是 datetime 类型）
df["Date"] = pd.to_datetime(df["Date"])
df["Year"] = df["Date"].dt.year

# 按年汇总总销售额
yearly_sales = df.groupby("Year")["Sales"].sum().reset_index()

# 构建 TypeScript 格式内容
ts_lines = ["export const salesData = ["]
for _, row in yearly_sales.iterrows():
    year = row["Year"]
    sales = int(row["Sales"])
    ts_lines.append(f'  {{ year: "{year}", sales: {sales} }},')
ts_lines.append("];")

# 写入 .ts 文件
with open("salesData.ts", "w", encoding="utf-8") as f:
    f.write("\n".join(ts_lines))

"✅ 已生成年销售额数据文件：src/data/salesData.ts"
