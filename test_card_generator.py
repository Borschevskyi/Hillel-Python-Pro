import unittest
from datetime import datetime
from card_generator import CardGeneration


class CardGenerationTests(unittest.TestCase):
    def test_generate_random_pan(self):
        pan = CardGeneration.generate_random_pan()
        self.assertEqual(len(pan), 16)
        self.assertTrue(pan.isdigit())

    def test_generate_random_expiration_date(self):
        expiration_date = CardGeneration.generate_random_expiration_date()
        self.assertRegex(expiration_date, r"\d{2}/\d{2}")
        month, year = expiration_date.split("/")
        self.assertTrue(month.isdigit())
        self.assertTrue(year.isdigit())
        self.assertTrue(1 <= int(month) <= 12)
        self.assertTrue(23 <= int(year) <= 30)

    def test_generate_random_cvv(self):
        cvv = CardGeneration.generate_random_cvv()
        self.assertEqual(len(cvv), 3)
        self.assertTrue(cvv.isdigit())

    def test_generate_random_issue_date(self):
        issue_date = CardGeneration.generate_random_issue_date()
        self.assertIsInstance(issue_date, str)
        self.assertRegex(issue_date, r"\d{4}-\d{2}-\d{2}")
        parsed_date = datetime.strptime(issue_date, "%Y-%m-%d")
        self.assertIsInstance(parsed_date, datetime)

    def test_generate_random_owner_id(self):
        owner_id = CardGeneration.generate_random_owner_id()
        self.assertRegex(owner_id, r"\w{8}-\w{4}-\w{4}-\w{4}-\w{12}")


if __name__ == "__main__":
    unittest.main()
