from typing import Optional

from euro_diffusion.city import City
from euro_diffusion.point import Point


class Country:
    def __init__(self, name: str, xl: int, yl: int, xh: int, yh: int) -> None:
        self.name = name
        self.cities = [
            City(self, x, y)
            for y in range(yl, yh + 1)
            for x in range(xl, xh + 1)
        ]
        self.bottom_left = Point(xl, yl)
        self.top_right = Point(xh, yh)
        self.complete_cities = 0
        self.completion_day: Optional[int] = None

    def init(self, initial_balance: int, completion_state: bool=False):
        for city in self.cities:
            city.balance = initial_balance
            city.cached_income = 0

        if completion_state:
            self.complete_cities = len(self.cities)
            self.completion_day = 0
        else:
            self.complete_cities = 0
            self.completion_day = None

    def add_complete_city(self, day: int):
        self.complete_cities += 1
        if self.complete_cities == len(self.cities):
            self.completion_day = day
