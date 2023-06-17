import unittest
import uuid
from unittest import mock
from unittest.mock import patch

from card import Card
from card_controller import CardController
from card_serializer import CardSerializer


class CardControllerTestCase(unittest.TestCase):
    @patch("card_controller.CardRepository")
    def test_set_existing_card(self, mock_repository):
        mock_instance = mock_repository.return_value
        existing_card = Card(
            "0000000000000001", "01/21", "012", "2021-01-21", str(uuid.uuid4()), 'new'
        )
        mock_instance.get_card_by_pan.return_value = existing_card
        controller = CardController()
        controller.set(
            existing_card.pan,
            existing_card.expiration_date,
            existing_card.cvv,
            existing_card.issue_date,
            existing_card.user_id,
            existing_card.status,
        )
        mock_instance.update_card.assert_called_once()

    @mock.patch("card_controller.CardRepository")
    def test_get_cards(self, mock_repository):
        mock_instance = mock_repository.return_value
        cards = [
            Card(
                "1111111111111112",
                "02/22",
                "123",
                "2022-02-22",
                str(uuid.uuid4()),
                "active",

            ),
            Card(
                "2222222222222223",
                "03/23",
                "234",
                "2023-03-23",
                str(uuid.uuid4()),
                'blocked',
            ),
        ]
        mock_instance.get_cards.return_value = cards
        controller = CardController()
        serializer = CardSerializer()
        expected_result = [serializer.to_json(card) for card in cards]
        result = controller.get()
        self.assertEqual(len(result), 2)
        self.assertEqual(result, expected_result)

    @patch("card_controller.CardRepository")
    def test_activate_blocked_card(self, mock_repository):
        mock_instance = mock_repository.return_value
        existing_card = Card(
            "3333333333333334",
            "04/24",
            "345",
            "2024-04-24",
            str(uuid.uuid4()),
            'blocked',
        )
        mock_instance.get_card_by_pan.return_value = existing_card
        controller = CardController()

        with patch("builtins.print") as mock_print:
            controller.activate_card("3333333333333334")
            mock_print.assert_not_called()

        mock_instance.update_card.assert_not_called()
        self.assertEqual(existing_card.status, 'blocked')

    @patch("card_controller.CardRepository")
    def test_activate_new_card(self, mock_repository):
        mock_instance = mock_repository.return_value
        existing_card = Card(
            "3333333333333335", "05/25", "555", "2025-05-25", str(uuid.uuid4()), 'new'
        )
        mock_instance.get_card_by_pan.return_value = existing_card
        controller = CardController()

        with patch("builtins.print") as mock_print:
            controller.activate_card("3333333333333335")
            mock_print.assert_not_called()

        mock_instance.update_card.assert_called_once()
        self.assertEqual(existing_card.status, 'active')

    @patch("card_controller.CardRepository")
    def test_activate_nonexistent_card(self, mock_repository):
        mock_instance = mock_repository.return_value
        mock_instance.get_card_by_pan.return_value = None
        controller = CardController()

        with patch("builtins.print") as mock_print:
            controller.activate_card("0000000000000001")

    @patch("card_controller.CardRepository")
    def test_block_existing_card(self, mock_repository):
        mock_instance = mock_repository.return_value
        existing_card = Card(
            "4444444444444445",
            "05/25",
            "456",
            "2025-05-25",
            str(uuid.uuid4()),
            'active',
        )
        mock_instance.get_card_by_pan.return_value = existing_card
        controller = CardController()
        controller.block_card("4444444444444445")
        mock_instance.update_card.assert_called_once()
        self.assertEqual(existing_card.status, 'blocked')

    @patch("card_controller.CardRepository")
    def test_block_nonexistent_card(self, mock_repository):
        mock_instance = mock_repository.return_value
        mock_instance.get_card_by_pan.return_value = None
        controller = CardController()

        with patch("builtins.print") as mock_print:
            controller.block_card("4444444444444446")

        mock_instance.get_card_by_pan.assert_called_once_with(
            "4444444444444446")


if __name__ == "__main__":
    unittest.main()
