from flask import Flask, jsonify, request

from card_controller import CardController
from card_repository import CardRepository
from card_serializer import CardSerializer

app = Flask(__name__)


@app.route("/create_card", methods=["GET"])
def create_card():
    CardRepository().create_table_cards()
    card = CardController.create_card()
    CardRepository().save_card(card)
    return jsonify({"message": "Card created successfully", "uuid": card.owner_id}), 201


@app.route("/get_card", methods=["GET"])
def get_card():
    owner_id = request.args.get("uuid")

    if owner_id is None:
        return jsonify({"message": "UUID parameter is missing"}), 400

    card = CardRepository().get_card_by_uuid(owner_id)

    if card is None:
        return jsonify({"message": "Card not found"}), 404

    card_data = CardSerializer.to_json(card)
    return jsonify(card_data), 200


if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
