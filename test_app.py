import unittest

from app import app


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_create_card(self):
        response = self.app.get("/create_card")
        self.assertEqual(response.status_code, 201)

    def test_get_card(self):
        create_response = self.app.get("/create_card")
        self.assertEqual(create_response.status_code, 201)
        owner_id = create_response.json["uuid"]

        response = self.app.get(f"/get_card?uuid={owner_id}")
        self.assertEqual(response.status_code, 200)

    def test_get_card_missing_uuid(self):
        response = self.app.get("/get_card")
        self.assertEqual(response.status_code, 400)

    def test_get_card_invalid_uuid(self):
        response = self.app.get("/get_card?uuid=invalid_uuid")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
