import unittest
import uuid
from card import Card


class TestCard(unittest.TestCase):
    def test_activate(self):
        card = Card(
            "1234567890123456",
            "12/25",
            "123",
            "2022-01-01",
            str(uuid.uuid4()),
            'new',
        )
        card.activate()
        self.assertEqual(card.status, 'active')

    def test_block(self):
        card = Card(
            "1234567890123456",
            "12/25",
            "123",
            "2022-01-01",
            str(uuid.uuid4()),
            'new',
        )
        card.block()
        self.assertEqual(card.status, 'blocked')

    def test_activate_blocked(self):
        card = Card(
            "1234567890123456",
            "12/25",
            "123",
            "2022-01-01",
            str(uuid.uuid4()),
            'blocked',
        )
        card.activate()
        self.assertEqual(card.status, 'blocked')


if __name__ == "__main__":
    unittest.main()
