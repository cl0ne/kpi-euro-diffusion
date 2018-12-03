
class City:
    def __init__(self, country, x: int, y: int):
        self.country: 'Country' = country
        self.x = x
        self.y = y
        self.balance = 0
        self.cached_income = 0

    @property
    def is_empty(self):
        return self.balance == 0 and self.cached_income == 0

    def add_income(self, amount: int):
        self.cached_income += amount

    def update_balance(self):
        self.balance += self.cached_income
        self.cached_income = 0
