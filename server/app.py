from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# manage cross-origin issues
CORS(app)
migrate = Migrate(app, db)

db.init_app(app)


@app.route("/")
def home():
    return "ChatBox"


@app.route('/messages', methods=["GET", "POST"])
def messages():

    if request.method == "GET":
        messages_lc = [message.to_dict() for message in Message.query.all()]
        return jsonify(messages_lc), 200

    elif request.method == "POST":
        data = request.get_json()
        new_message = Message(
            body=data["body"],
            username=data["username"]
        )
        db.session.add(new_message)
        db.session.commit()
        new_message_dict = new_message.to_dict()
        return jsonify(new_message_dict), 201


@app.route('/messages/<int:id>', methods=["PATCH", "DELETE"])
def messages_by_id(id):
    message = Message.query.get(id)

    if not message:
        return jsonify({"error": "Message not found"}), 404

    if request.method == "PATCH":
        updated_message = request.get_json()

        for attr in updated_message:
            setattr(message, attr, updated_message.get(attr))

        db.session.commit()

        message_dict = message.to_dict()

        return jsonify(message_dict), 200

    elif request.method == "DELETE":
        db.session.delete(message)
        db.session.commit()

        response_body = {
            "success": True,
            "message": "Message deleted"
        }

        return jsonify(response_body), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)

