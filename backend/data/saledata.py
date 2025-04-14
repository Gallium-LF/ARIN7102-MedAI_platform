import pandas as pd

# 修改为你的实际 CSV 文件路径
csv_path = "backend/data/customer_purchase_data.csv"

# 读取数据
data = pd.read_csv(csv_path)

# 保证字段存在
required_columns = ["Age", "Gender", "ProductCategory", "PurchaseStatus"]
for col in required_columns:
    if col not in data.columns:
        raise ValueError(f"Missing column: {col}")

# ✅ 1. 产品种类购买率
product_group = data.groupby("ProductCategory")["PurchaseStatus"]
product_purchase_rate = (product_group.sum() / product_group.count()).round(4).to_dict()

# ✅ 2. 性别购买率
gender_group = data.groupby("Gender")["PurchaseStatus"]
gender_purchase_rate = (gender_group.sum() / gender_group.count()).round(4).to_dict()

# ✅ 3. 年龄段购买率（每10岁为一段）
data["AgeGroup"] = (data["Age"] // 10) * 10
age_group = data.groupby("AgeGroup")["PurchaseStatus"]
age_purchase_rate = (age_group.sum() / age_group.count()).round(4).to_dict()

# ✅ 输出结果
print("✅ Product Category Purchase Rate:")
print(product_purchase_rate)

print("\n✅ Gender Purchase Rate:")
print(gender_purchase_rate)

print("\n✅ Age Group Purchase Rate (10-year bins):")
print(age_purchase_rate)
