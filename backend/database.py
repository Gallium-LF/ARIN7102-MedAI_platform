from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://root:123456@localhost/aiask?charset=utf8mb4"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Conversation(db.Model):
    __tablename__ = "conversation"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    messages = db.relationship(
        "Message", backref="conversation", cascade="all, delete-orphan"
    )
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    last_updated = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )


class Message(db.Model):
    __tablename__ = "message"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    conversation_id = db.Column(
        db.Integer, db.ForeignKey("conversation.id", ondelete="CASCADE"), nullable=False
    )
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return "Hello, Flask with MySQL!"


if __name__ == "__main__":
    app.run(debug=True)
