from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from chatapi import chatapi,chatapi_test
from sqlalchemy import desc
from datetime import datetime
from sentence_transformers import SentenceTransformer
import faiss
import pickle
import torch

from database import db, Conversation, Message

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://root:123456@localhost:3306/aiask?charset=utf8mb4"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

_device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {_device}")

# 指定模型和设备
_model = SentenceTransformer(
    "all-MiniLM-L6-v2", device="cuda" if torch.cuda.is_available() else "cpu"
)

# 三个向量库配置（路径）
VECTOR_SOURCES = {
    "user_behavior": {
        "index": "backend/user_behavior.index",
        "pkl": "backend/user_behavior.pkl",
    },
    "store_sales": {
        "index": "backend/store_sales.index",
        "pkl": "backend/store_sales.pkl",
    },
    "drug_reviews": {
        "index": "backend/drug_reviews.index",
        "pkl": "backend/id_to_text.pkl",
    },
}

# 加载所有向量库（一次性）
_loaded_indexes = {}
for name, paths in VECTOR_SOURCES.items():
    idx = faiss.read_index(paths["index"])
    with open(paths["pkl"], "rb") as f:
        txts = pickle.load(f)
    _loaded_indexes[name] = (idx, txts)


# 多库检索函数
def retrieve_reviews_for_llm(user_query: str, top_k: int = 10) -> str:
    query_embedding = _model.encode([user_query], convert_to_numpy=True)
    results = []

    for source_name, (index, texts) in _loaded_indexes.items():
        D, I = index.search(query_embedding, top_k)

        section = [f"=== Source: {source_name} ==="]
        for rank, i in enumerate(I[0]):
            section.append(f"{rank + 1}. {texts[i]}")
        results.append("\n".join(section))

    return "\n\n".join(results)


def build_prompt(user_question: str, retrieved_context: str) -> str:
    """
    构建药品销售建议助手使用的大模型 Prompt。
    """
    prompt = f"""You are a helpful AI assistant who is answering a question using structured information retrieved from different data sources.

Below are the relevant records retrieved from multiple sources:

{retrieved_context}

Your task is to analyze the provided information and answer the user's question as accurately as possible.
If some records are not useful for answering the question, simply ignore them without commenting on their relevance.

Be concise and focus your answer based only on useful information.

User Question: {user_question}

Answer:"""
    return prompt


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")
    conversation_id = data.get("conversation_id")

    if not user_message:
        return jsonify({"error": "Missing message"}), 400
    reviews=retrieve_reviews_for_llm(user_message)
    prompt = build_prompt(user_message, reviews)
    ai_response = chatapi(prompt)

    if conversation_id:
        conversation = Conversation.query.get(conversation_id)
        if not conversation:
            return jsonify({"error": "Conversation not found"}), 404

        conversation.last_updated = datetime.now()
    else:
        conversation = Conversation()
        db.session.add(conversation)
        db.session.commit()

    message = Message(
        conversation_id=conversation.id,
        question=user_message,
        answer=ai_response,
    )
    db.session.add(message)

    db.session.commit()

    return jsonify({"reply": ai_response, "conversation_id": conversation.id})


@app.route("/chat/history", methods=["GET"])
def get_chat_history():
    conversations = Conversation.query.order_by(desc(Conversation.last_updated)).all()
    all_conversations = []

    for conv in conversations:
        messages = Message.query.filter_by(conversation_id=conv.id).all()
        message_list = [
            {
                "question": msg.question,
                "answer": msg.answer,
            }
            for msg in messages
        ]
        all_conversations.append(
            {
                "conversation_id": conv.id,
                "created_at": conv.created_at,
                "last_updated": conv.last_updated,
                "messages": message_list,
            }
        )

    return jsonify(all_conversations)


@app.route("/chat/delete/<int:conversation_id>", methods=["DELETE"])
def delete_conversation(conversation_id):
    conversation = Conversation.query.get(conversation_id)
    if not conversation:
        return jsonify({"error": "Conversation not found"}), 404

    db.session.delete(conversation)
    db.session.commit()
    return jsonify({"message": "Conversation deleted successfully"})


if __name__ == "__main__":
    app.run(debug=True)
