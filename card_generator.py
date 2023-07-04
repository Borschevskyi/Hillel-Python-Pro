import random
import string
from datetime import date
from uuid import uuid4


class CardGeneration:
    @classmethod
    def generate_random_pan(cls):
        digits = string.digits
        return "".join(random.choices(digits, k=16))

    @classmethod
    def generate_random_expiration_date(cls):
        months = [str(i).zfill(2) for i in range(1, 13)]
        years = [str(i).zfill(2) for i in range(23, 31)]
        return random.choice(months) + "/" + random.choice(years)

    @classmethod
    def generate_random_cvv(cls):
        digits = string.digits
        return "".join(random.choices(digits, k=3))

    @classmethod
    def generate_random_issue_date(cls):
        today = date.today()
        return today.strftime("%Y-%m-%d")

    @classmethod
    def generate_random_owner_id(cls):
        owner_id = str(uuid4())
        return owner_id
