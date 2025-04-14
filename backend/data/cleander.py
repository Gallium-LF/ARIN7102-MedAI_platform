import pandas as pd
import datetime as dt

# CSV 路径
csv_path = "backend/data/train.csv"

# 读取数据
df = pd.read_csv(csv_path)

# 只保留开店记录并转换日期
df = df[df["Open"] == 1].copy()
df["Date"] = pd.to_datetime(df["Date"])

# 限制时间范围：2015-01-01 至 2015-07-31
start_date = pd.to_datetime("2015-01-01")
end_date = pd.to_datetime("2015-07-31")
df = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]

# 按日期汇总每天总销售额
daily_sales = df.groupby("Date")["Sales"].sum().reset_index()

# 生成 week/day 格式
daily_sales["Week"] = daily_sales["Date"].apply(lambda d: d.isocalendar()[1])
daily_sales["Day"] = daily_sales["Date"].dt.day_name()
daily_sales["DateStr"] = daily_sales["Date"].dt.strftime("%Y-%m-%d")

# 构建 TypeScript 数据
ts_lines = ["export const heatmapCalendarData = ["]
for _, row in daily_sales.iterrows():
    week = row["Week"]
    day = row["Day"]
    date = row["DateStr"]
    sales = int(row["Sales"])
    ts_lines.append(
        f'  {{ week: "{week}", day: "{day}", date: "{date}", sales: {sales} }},'
    )
ts_lines.append("];")

# 写入 .ts 文件
with open("./heatmapCalendarData.ts", "w", encoding="utf-8") as f:
    f.write("\n".join(ts_lines))

"✅ 日历热力图数据 heatmapCalendarData.ts 已生成，可用于 G2Plot Heatmap 渲染。"
