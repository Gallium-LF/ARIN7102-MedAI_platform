import pandas as pd
import numpy as np
import faiss
import pickle
from sentence_transformers import SentenceTransformer

# === 1. 加载原始数据 ===
csv_path = "backend/data/customer_purchase_data.csv"  # 改成你的CSV路径
df = pd.read_csv(csv_path)


# === 2. 每一行转换为结构化自然语言 ===
def row_to_text(row):
    gender = "Male" if row["Gender"] == 1 else "Female"
    loyalty = "Yes" if row["LoyaltyProgram"] == 1 else "No"
    discount = "Yes" if row["DiscountsAvailed"] == 1 else "No"
    purchased = "Purchased" if row["PurchaseStatus"] == 1 else "Not Purchased"

    return (
        f"User is {row['Age']} years old, "
        f"Gender: {gender}, "
        f"Annual Income: {row['AnnualIncome']:.2f}, "
        f"Number of Purchases: {row['NumberOfPurchases']}, "
        f"Product Category: {row['ProductCategory']}, "
        f"Time Spent on Website: {row['TimeSpentOnWebsite']:.2f} minutes, "
        f"Loyalty Program: {loyalty}, "
        f"Discount Availed: {discount}, "
        f"Purchase Status: {purchased}."
    )


texts = df.apply(row_to_text, axis=1).tolist()

# === 3. 嵌入向量模型 ===
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(texts, convert_to_numpy=True)

# === 4. 构建 FAISS 索引 ===
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# === 5. 保存 FAISS 索引和文本 ===
faiss.write_index(index, "user_behavior.index")
with open("user_behavior.pkl", "wb") as f:
    pickle.dump(texts, f)

print("Index and text list saved!")


# === 6. 检索函数：给一个问题返回最相关的句子 ===
def search_top_k(query, k=5):
    query_vec = model.encode([query], convert_to_numpy=True)
    D, I = index.search(query_vec, k)
    return [texts[i] for i in I[0]]


# ✅ 示例：
if __name__ == "__main__":
    results = search_top_k("Who are the most active female customers?")
    print("🔍 Top results:")
    for r in results:
        print("-", r)
