from dotenv import load_dotenv

from card import Card
from card_generator import CardGeneration
from card_repository import CardRepository
from card_serializer import CardSerializer

load_dotenv()


class CardController:
    def __init__(self):
        self.serializer = CardSerializer()
        self.connection = CardRepository()

    def set_card(self, pan, expiration_date, cvv, issue_date, owner_id, status):
        existing_card = self.connection.get_card_by_pan(pan)
        if existing_card:
            existing_card.status = status
            self.connection.update_card(existing_card)
        else:
            card = Card(pan, expiration_date, cvv, issue_date, owner_id, status)
            self.connection.save_card(card)

    def get_card(self):
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

    @staticmethod
    def create_card():
        pan = CardGeneration.generate_random_pan()
        expiration_date = CardGeneration.generate_random_expiration_date()
        cvv = CardGeneration.generate_random_cvv()
        issue_date = CardGeneration.generate_random_issue_date()
        owner_id = CardGeneration.generate_random_owner_id()
        status = "new"
        card = Card(pan, expiration_date, cvv, issue_date, owner_id, status)
        return card
