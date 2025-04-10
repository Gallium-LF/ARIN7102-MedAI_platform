import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from tqdm import tqdm
import pickle

df = pd.read_csv("backend/data/merged_file.csv")


def format_entry(row):
    return (
        f"Drug: {row['drugName']}\n"
        f"Condition: {row['condition']}\n"
        f"Review: {row['review']}\n"
        f"Rating: {row['rating']}\n"
        f"Date: {row['date']}\n"
        f"Useful Votes: {row['usefulCount']}"
    )


texts = [format_entry(row) for _, row in tqdm(df.iterrows(), total=len(df))]

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)

embedding_dim = embeddings.shape[1]
index = faiss.IndexFlatL2(embedding_dim)
index.add(embeddings)

faiss.write_index(index, "./drug_reviews.index")

with open("id_to_text.pkl", "wb") as f:
    pickle.dump(texts, f)

print("✅ 向量化完成并已保存至 'drug_reviews.index' 和 'id_to_text.pkl'")
