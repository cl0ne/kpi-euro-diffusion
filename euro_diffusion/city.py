
class City:
    def __init__(self, country, x, y):
        self.country: 'Country' = country
        self.x = x
        self.y = y
        self.balance = 0
        self.cached_income = 0
