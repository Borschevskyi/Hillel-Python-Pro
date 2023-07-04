import json

from card import Card


class CardSerializer:
    @classmethod
    def to_json(cls, card: Card) -> str:
        return json.dumps(
            {
                "pan": card.pan,
                "expiration_date": card.expiration_date,
                "cvv": card.cvv,
                "issue_date": card.issue_date,
                "owner_id": card.owner_id,
                "status": card.status,
            }
        )
