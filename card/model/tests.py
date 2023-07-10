import json
import uuid
from django.test import TestCase
from django.urls import reverse
from model.models import Cards


class CardTest(TestCase):
    def test_get(self):
        owner_id = uuid.uuid4()
        cards = Cards(
            pan="1234567890123456",
            expiration_date="12/24",
            cvv="123",
            owner_id=str(owner_id),
            status="new",
        )
        cards.save()
        url = reverse("card")
        response = self.client.get(url, HTTP_ACCEPT="application/json").json()

        self.assertEqual(
            response,
            {
                "cards": [
                    {
                        "pan": "1234567890123456",
                        "expiration_date": "12/24",
                        "cvv": "123",
                        "owner_id": str(owner_id),
                        "status": "new",
                    }
                ]
            },
        )

    def test_post(self):
        url = reverse("card")
        data = {
            "pan": "1234567890123456",
            "expiration_date": "12/24",
            "cvv": "123",
            "status": "new",
        }
        response = self.client.post(
            url, json.dumps(data), content_type="application/json"
        )
        response_data = json.loads(response.content)

        card_id = response_data.get("id")
        card = Cards.objects.filter(id=card_id).first()

        self.assertIsNotNone(card)
        self.assertEqual(card.pan, data["pan"])
        self.assertEqual(card.expiration_date, data["expiration_date"])
        self.assertEqual(card.cvv, data["cvv"])
        self.assertEqual(card.status, data["status"])

    def test_is_valid(self):
        valid_card = "4441114454441013"
        card = Cards.objects.create(
            pan = valid_card,
            expiration_date = "05/29",
            cvv = "123",
            owner_id = str(uuid.uuid4()),
            status = "new",
        )

        is_valid = card.is_valid(valid_card)
        print(f"Card Number: {valid_card}, Is Valid: {is_valid}")
        self.assertTrue(is_valid)

        invalid_card = "8531462222641434"
        card = Cards.objects.create(
            pan = invalid_card,
            expiration_date = "12/24",
            cvv = "123",
            owner_id = str(uuid.uuid4()),
            status = "new",
        )

        is_valid = card.is_valid(invalid_card)
        print(f"Card Number: {invalid_card}, Is Valid: {is_valid}")
        self.assertFalse(is_valid)
