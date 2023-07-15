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
        return [int(digit) for digit in str(number) if digit.isdigit()]

    def is_valid(self, card_number: str) -> bool:
        card = Cards.objects.get(pan = card_number)
        digits = self.digits_on(card_number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        check_sum = sum(odd_digits)
        for even_number in even_digits:
            multiplied_digits = self.digits_on(even_number * 2)
            check_sum += sum(multiplied_digits)
        is_valid = check_sum % 10 == 0
        print(f"Card number: {card_number}, Checksum: {check_sum}, Is Valid: {is_valid}")
        return is_valid
