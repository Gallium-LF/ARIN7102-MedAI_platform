import pandas as pd
import datetime as dt

csv_path = "backend/data/train.csv"

df = pd.read_csv(csv_path)

df = df[df["Open"] == 1].copy()
df["Date"] = pd.to_datetime(df["Date"])

start_date = pd.to_datetime("2015-01-01")
end_date = pd.to_datetime("2015-07-31")
df = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]

daily_sales = df.groupby("Date")["Sales"].sum().reset_index()

daily_sales["Week"] = daily_sales["Date"].apply(lambda d: d.isocalendar()[1])
daily_sales["Day"] = daily_sales["Date"].dt.day_name()
daily_sales["DateStr"] = daily_sales["Date"].dt.strftime("%Y-%m-%d")

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

with open("./heatmapCalendarData.ts", "w", encoding="utf-8") as f:
    f.write("\n".join(ts_lines))

