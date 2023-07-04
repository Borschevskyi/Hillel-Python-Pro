import os
import unittest
import uuid
from unittest.mock import patch
from card_repository import CardRepository
from card import Card


class CardRepositoryTestCase(unittest.TestCase):
    @patch("builtins.input", side_effect=["123"])
    def setUp(self, mock_input):
        self.card_repository = CardRepository()
        self.card_repository.create_table_cards()

    def tearDown(self):
        self.card_repository.close()

    @patch("builtins.input", side_effect=["123"])
    def test_save_card(self, mock_input):
        card_repository = CardRepository()
        card_repository.create_table_cards()
        card = Card(
            "0000000000000001", "01/21", "012", "2021-01-21", str(uuid.uuid4()), "new"
        )
        card_repository.save_card(card)
        saved_card = card_repository.get_card_by_pan(card.pan)
        self.assertEqual(saved_card.pan, card.pan)
        self.assertEqual(saved_card.expiration_date, card.expiration_date)
        self.assertEqual(saved_card.cvv, card.cvv)
        self.assertEqual(saved_card.issue_date, card.issue_date)
        self.assertEqual(saved_card.status, card.status)

    @patch("builtins.input", side_effect=["123"])
    def test_get_cards(self, mock_input):
        card_repository = CardRepository()
        card_repository.create_table_cards()
        card1 = Card(
            "1111111111111112",
            "02/22",
            "123",
            "2022-02-22",
            str(uuid.uuid4()),
            "active",
        )
        card2 = Card(
            "2222222222222223",
            "03/23",
            "234",
            "2023-03-23",
            str(uuid.uuid4()),
            "blocked",
        )
        card_repository.save_card(card1)
        card_repository.save_card(card2)
        cards = card_repository.get_cards()
        self.assertEqual(len(cards), 6)
        self.assertEqual(cards[4].pan, "1111111111111112")
        self.assertEqual(cards[5].pan, "2222222222222223")

    @patch("builtins.input", side_effect=["123"])
    def test_get_card_by_pan(self, mock_input):
        card_repository = CardRepository()
        card_repository.create_table_cards()
        card = Card(
            "3333333333333334",
            "04/24",
            "345",
            "2024-04-24",
            str(uuid.uuid4()),
            "active",
        )
        card_repository.save_card(card)
        retrieved_card = card_repository.get_card_by_pan("3333333333333334")
        self.assertEqual(retrieved_card.pan, card.pan)
        self.assertEqual(retrieved_card.expiration_date, card.expiration_date)
        self.assertEqual(retrieved_card.cvv, card.cvv)
        self.assertEqual(retrieved_card.issue_date, card.issue_date)
        self.assertEqual(retrieved_card.owner_id, card.owner_id)
        self.assertEqual(retrieved_card.status, card.status)

    @patch("builtins.input", side_effect=["123"])
    def test_get_card_by_uuid(self, mock_input):
        card_repository = CardRepository()
        card_repository.create_table_cards()
        owner_id = str(uuid.uuid4())
        card = Card(
            "3333333333333335",
            "04/24",
            "345",
            "2024-04-24",
            owner_id,
            "active",
        )
        card_repository.save_card(card)
        retrieved_card = card_repository.get_card_by_uuid(owner_id)
        self.assertEqual(retrieved_card.pan, card.pan)
        self.assertEqual(retrieved_card.expiration_date, card.expiration_date)
        self.assertEqual(retrieved_card.cvv, card.cvv)
        self.assertEqual(retrieved_card.issue_date, card.issue_date)
        self.assertEqual(retrieved_card.owner_id, card.owner_id)
        self.assertEqual(retrieved_card.status, card.status)

    @patch("builtins.input", side_effect=["123"])
    def test_update_card(self, mock_input):
        card_repository = CardRepository()
        card_repository.create_table_cards()
        card = Card(
            "4444444444444445",
            "05/25",
            "456",
            "2025-05-25",
            str(uuid.uuid4()),
            "active",
        )
        card_repository.save_card(card)
        card.expiration_date = "06/26"
        card.cvv = "567"
        card.issue_date = "2026-06-26"
        card.status = "blocked"
        card_repository.update_card(card)
        updated_card = card_repository.get_card_by_pan(card.pan)
        self.assertEqual(updated_card.expiration_date, card.expiration_date)
        self.assertEqual(updated_card.cvv, card.cvv)
        self.assertEqual(updated_card.issue_date, card.issue_date)
        self.assertEqual(updated_card.status, card.status)


if __name__ == "__main__":
    unittest.main()
