from dotenv import load_dotenv
import uuid

from card import Card
from card_repository import CardRepository
from card_serializer import CardSerializer

load_dotenv()


class CardController:
    def __init__(self):
        self.serializer = CardSerializer()
        self.connection = CardRepository()
        self.card = Card

    def set(self, pan, expiration_date, cvv, issue_date, user_id, status):
        existing_card = self.connection.get_card_by_pan(pan)
        if existing_card:
            existing_card.status = status
            self.connection.update_card(existing_card)
        else:
            card = Card(pan, expiration_date, cvv, issue_date, user_id, status)
            self.connection.save_card(card)

    def get(self):
        cards = self.connection.get_cards()
        return [self.serializer.to_json(card) for card in cards]

    def activate_card(self, pan):
        card = self.connection.get_card_by_pan(pan)
        if card:
            if card.status == 'new':
                card.activate()
                self.connection.update_card(card)

    def block_card(self, pan):
        card = self.connection.get_card_by_pan(pan)
        if card:
            card.block()
            self.connection.update_card(card)


# if __name__ == "__main__":
#     controller = CardController()
#
#     serializer = CardSerializer()
#
#     controller.connection.create_table()
#
#     controller.set(
#         "5168111122220912", "06/25", "016", "2023-06-14", str(uuid.uuid4()), "new"
#     )
#
#     print(controller.get())
#     controller.activate_card("5168111122220912")
#     print(controller.get())
#     controller.block_card("5168111122220912")
#     print(controller.get())
#     controller.activate_card("5168111122220912")
#     print(controller.get())
