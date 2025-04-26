import pandas as pd

df = pd.read_csv("backend/data/train.csv")

n_per_date = 5

df_sampled = df.groupby("Date").apply(
    lambda x: x.sample(n=min(n_per_date, len(x)), random_state=42)
)

df_sampled.reset_index(drop=True, inplace=True)

df_sampled.to_csv("backend/data/sampled_data.csv", index=False)

