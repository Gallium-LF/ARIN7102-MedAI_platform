import pandas as pd
import numpy as np
import faiss
import pickle
from sentence_transformers import SentenceTransformer

df = pd.read_csv("backend/data/sampled_data.csv")


def row_to_text(row):
    state_holiday = (
        "a state holiday"
        if row["StateHoliday"] in [1, "1", "a"]
        else "not a state holiday"
    )
    school_holiday = (
        "a school holiday"
        if row["SchoolHoliday"] == 1 or row["SchoolHoliday"] == "1"
        else "not a school holiday"
    )
    open_status = "was open" if row["Open"] == 1 else "was closed"
    promo_status = "with a promotion" if row["Promo"] == 1 else "without promotion"

    return (
        f"On {row['Date']}, store {row['Store']} {open_status} {promo_status}. "
        f"It had {row['Customers']} customers and made {row['Sales']} in sales. "
        f"It was {school_holiday} and {state_holiday}."
    )


texts = df.apply(row_to_text, axis=1).tolist()

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(texts, convert_to_numpy=True)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

faiss.write_index(index, "store_sales.index")
with open("store_sales.pkl", "wb") as f:
    pickle.dump(texts, f)

def search_top_k(query, k=5):
    query_embedding = model.encode([query], convert_to_numpy=True)
    D, I = index.search(query_embedding, k)
    return [texts[i] for i in I[0]]

if __name__ == "__main__":
    query = "How did store 102 perform during holidays?"
    results = search_top_k(query)
    print("🔍 Top results:")
    for r in results:
        print("-", r)
