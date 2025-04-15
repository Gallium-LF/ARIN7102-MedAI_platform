import pandas as pd

# 读取数据（加上正确路径）
df = pd.read_csv("backend/data/train.csv")

# 每个日期保留的记录数量
n_per_date = 5  # 你可以调大调小

# 分组抽样
df_sampled = df.groupby("Date").apply(
    lambda x: x.sample(n=min(n_per_date, len(x)), random_state=42)
)

# 去掉 groupby 自动添加的索引
df_sampled.reset_index(drop=True, inplace=True)

# 保存结果
df_sampled.to_csv("backend/data/sampled_data.csv", index=False)

print("✅ 已保存压缩后的数据集 sampled_data.csv")
