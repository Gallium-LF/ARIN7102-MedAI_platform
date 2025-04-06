from flask import Flask, request, jsonify
from flask_cors import CORS  # 跨域支持（重要，允许前端访问）
from flask_sqlalchemy import SQLAlchemy
from chatapi import chatapi,chatapi_test  # 引入你的 AI 聊天逻辑
from sqlalchemy import desc  # 导入 desc 方法
from datetime import datetime

from database import db, Conversation, Message

app = Flask(__name__)
CORS(app)  # 允许跨域请求（前端 Vue 能访问）
# 配置 MySQL 数据库
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://root:123456@localhost:3306/aiask?charset=utf8mb4"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # 关闭 SQLAlchemy 修改追踪

# 初始化数据库
db.init_app(app)


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")
    conversation_id = data.get("conversation_id")  # 可选参数

    if not user_message:
        return jsonify({"error": "Missing message"}), 400

    # 获取 AI 回复
    ai_response = chatapi(user_message)

    # ✅ 检查是否提供 conversation_id，如果存在则追加
    if conversation_id:
        conversation = Conversation.query.get(conversation_id)
        if not conversation:
            return jsonify({"error": "Conversation not found"}), 404

        # ✅ 手动更新 last_updated 字段
        conversation.last_updated = datetime.now()
    else:
        # 创建新会话
        conversation = Conversation()
        db.session.add(conversation)
        db.session.commit()

    # ✅ 插入用户消息和 AI 回复
    message = Message(
        conversation_id=conversation.id,
        question=user_message,
        answer=ai_response,
    )
    db.session.add(message)

    # ✅ 提交更新
    db.session.commit()

    return jsonify({"reply": ai_response, "conversation_id": conversation.id})


# ✅ 查看所有聊天记录


@app.route("/chat/history", methods=["GET"])
def get_chat_history():
    # ✅ 使用 last_updated 字段进行降序排序
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


# ✅ 删除指定的会话
@app.route("/chat/delete/<int:conversation_id>", methods=["DELETE"])
def delete_conversation(conversation_id):
    conversation = Conversation.query.get(conversation_id)
    if not conversation:
        return jsonify({"error": "Conversation not found"}), 404

    # 删除会话及相关消息
    db.session.delete(conversation)
    db.session.commit()
    return jsonify({"message": "Conversation deleted successfully"})


if __name__ == "__main__":
    app.run(debug=True)
