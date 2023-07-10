import uuid
from django.db import models
from django.http import HttpRequest


class Cards(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pan = models.CharField(max_length=20)
    expiration_date = models.CharField(max_length=20)
    cvv = models.CharField(max_length=4)
    issue_date = models.DateTimeField(auto_now_add=True)
    owner_id = models.UUIDField(default=uuid.uuid4)
    status = models.CharField(max_length=10)

    def digits_on(self, number: str) -> list:
        return [int(digit) for digit in str(number)]

    def is_valid(self, request: HttpRequest) -> bool:
        card_number = Cards.objects.get(pan="1234567890123456")
        digits = self.digits_on(card_number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        check_sum = 0
        check_sum += sum(odd_digits)
        for even_numbers in even_digits:
            check_sum += sum(self.digits_on(even_numbers * 2))
        return check_sum % 10 == 0
