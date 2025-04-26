import pandas as pd

csv_path = "backend/data/customer_purchase_data.csv"

data = pd.read_csv(csv_path)

required_columns = ["Age", "Gender", "ProductCategory", "PurchaseStatus"]
for col in required_columns:
    if col not in data.columns:
        raise ValueError(f"Missing column: {col}")

product_group = data.groupby("ProductCategory")["PurchaseStatus"]
product_purchase_rate = (product_group.sum() / product_group.count()).round(4).to_dict()

gender_group = data.groupby("Gender")["PurchaseStatus"]
gender_purchase_rate = (gender_group.sum() / gender_group.count()).round(4).to_dict()

data["AgeGroup"] = (data["Age"] // 10) * 10
age_group = data.groupby("AgeGroup")["PurchaseStatus"]
age_purchase_rate = (age_group.sum() / age_group.count()).round(4).to_dict()

print("✅ Product Category Purchase Rate:")
print(product_purchase_rate)

print("\n✅ Gender Purchase Rate:")
print(gender_purchase_rate)

print("\n✅ Age Group Purchase Rate (10-year bins):")
print(age_purchase_rate)
