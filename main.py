#!/usr/bin/env python3

import sys
from typing import List, Tuple

from euro_diffusion.country import Country, Point, City


class Field:
    def __init__(self, w, h, default_value=None):
        self.w = w
        self.h = h
        self._data = [
            [default_value] * w
            for _ in range(h)
        ]

    def __getitem__(self, key):
        x, y = key
        return self._data[y][x]

    def __setitem__(self, key, value):
        x, y = key
        self._data[y][x] = value


class Region:
    def __init__(self, countries: List[Country]):
        self._countries = countries
        self._bottom_left, self._top_right = self._find_total_bounds()
        area_size = self._top_right - self._bottom_left + Point(1, 1)

        self._field = Field(area_size.x, area_size.y)
        self._city_count = 0

        # Fill field and recalculate object coordinates
        # to eliminate field coordinates calculation on every
        # iteration
        for c in countries:
            self._city_count += len(c.cities)
            c.bottom_left -= self._bottom_left
            c.top_right -= self._bottom_left

            for city in c.cities:
                city.x -= self._bottom_left.x
                city.y -= self._bottom_left.y
                self._field[city.x, city.y] = city

    def _find_total_bounds(self) -> Tuple[Point, Point]:
        first_country = self._countries[0]
        bottom_left, top_right = (
            first_country.bottom_left.clone(), first_country.top_right.clone()
        )
        for c in self._countries[1:]:
            bottom_left.x = min(bottom_left.x, c.bottom_left.x)
            bottom_left.y = min(bottom_left.y, c.bottom_left.y)
            top_right.x = max(top_right.x, c.top_right.x)
            top_right.y = max(top_right.y, c.top_right.y)
        return bottom_left, top_right

    def simulate(self):
        return [
            (country, self._simulate_country(i))
            for i, country in enumerate(self._countries)
        ]

    def _simulate_country(self, country_index):
        queue: List[City] = []
        for i, country in enumerate(self._countries):
            initial_balance = 0
            if i == country_index:
                initial_balance = 1000_000
                queue = country.cities.copy()
            for city in country.cities:
                city.balance = initial_balance
                city.cached_income = 0
        representative_factor = 1_000
        day = 0
        while True:
            new_cities = []
            for city in queue:
                representative_portion = city.balance // representative_factor
                if representative_portion == 0:
                    continue
                for n_x, n_y in self._get_neighbours(city.x, city.y):
                    neighbour: City = self._field[n_x, n_y]
                    if neighbour is None:
                        continue
                    if neighbour.balance == 0 and neighbour.cached_income == 0:
                        new_cities.append(neighbour)
                    city.cached_income -= representative_portion
                    neighbour.cached_income += representative_portion
            day += 1
            queue += new_cities
            for city in queue:
                city.balance += city.cached_income
                city.cached_income = 0

            if self._city_count == len(queue):
                break
        return day

    def _get_neighbours(self, x, y):
        # Left
        if x > 0:
            yield x - 1, y
        # Right
        if (x + 1) < self._field.w:
            yield x + 1, y
        # Up
        if y > 0:
            yield x, y - 1
        # Down
        if (y + 1) < self._field.h:
            yield x, y + 1


def main(argv):
    countries = [
        Country('France', 1, 4, 4, 6),
        Country('Spain', 3, 1, 6, 3),
        Country('Portugal', 1, 1, 2, 2)
    ]
    for c, d in Region(countries).simulate():
        print(c.name, ':', d)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
