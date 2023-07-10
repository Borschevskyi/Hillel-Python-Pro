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
