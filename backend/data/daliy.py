import pandas as pd

csv_path = "backend/data/train.csv"

df = pd.read_csv(csv_path)

df = df[df["Open"] == 1]

df["Date"] = pd.to_datetime(df["Date"])
df["Year"] = df["Date"].dt.year

yearly_sales = df.groupby("Year")["Sales"].sum().reset_index()

ts_lines = ["export const salesData = ["]
for _, row in yearly_sales.iterrows():
    year = row["Year"]
    sales = int(row["Sales"])
    ts_lines.append(f'  {{ year: "{year}", sales: {sales} }},')
ts_lines.append("];")

with open("salesData.ts", "w", encoding="utf-8") as f:
    f.write("\n".join(ts_lines))

