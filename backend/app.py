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

_model = SentenceTransformer("all-MiniLM-L6-v2", device=_device)
_index = faiss.read_index("backend/drug_reviews.index")
with open("backend/id_to_text.pkl", "rb") as f:
    _texts = pickle.load(f)


def retrieve_reviews_for_llm(user_query: str, top_k: int = 5) -> str:
    query_embedding = _model.encode([user_query], convert_to_numpy=True)

    D, I = _index.search(query_embedding, top_k)

    results = []
    for rank, i in enumerate(I[0]):
        results.append(f"Result {rank + 1}:\n{_texts[i]}")

    return "\n\n".join(results)


def build_prompt(user_question: str, retrieved_context: str) -> str:
    """
    构建药品销售建议助手使用的大模型 Prompt。
    """
    prompt = f"""You are a pharmaceutical sales assistant. Based on the following user reviews and feedback, help provide a drug recommendation that is popular, effective, and well-received.

Customer Question:
{user_question}

Relevant Drug Reviews:
{retrieved_context}

As a sales assistant, give your recommendation with reasons based on user opinions:"""
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
