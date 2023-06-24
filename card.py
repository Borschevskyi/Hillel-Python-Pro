class Card:
    ALLOWED_STATUSES = ["new", "active", "blocked"]

    def __init__(
        self,
        pan: str,
        expiration_date: str,
        cvv: str,
        issue_date: str,
        owner_id: str,
        status: ALLOWED_STATUSES,
    ) -> None:
        self.pan = pan
        self.expiration_date = expiration_date
        self.cvv = cvv
        self.issue_date = issue_date
        self.owner_id = owner_id
        self.status = status

    def activate(self):
        if self.status != 'blocked':
            self.status = 'active'

    def block(self):
        self.status = 'blocked'
