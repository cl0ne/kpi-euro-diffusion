from functools import reduce
from typing import List, Tuple, Iterable

from euro_diffusion.country import Country, Point, City

class Field:
    def __init__(self, rows, columns, default_value=None):
        self.rows = rows
        self.columns = columns
        self._data = [
            [default_value] * columns
            for _ in range(rows)
        ]

    def __getitem__(self, key):
        r, c = key
        return self._data[r][c]

    def __setitem__(self, key, value):
        r, c = key
        self._data[r][c] = value


class Simulator:
    _REPRESENTATIVE_FACTOR = 1_000
    _FULL_INITIAL_BALANCE = 1000_000

    def __init__(self, countries: List[Country]):
        self._countries = countries
        if len(countries) < 2:
            return

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

    def run(self) -> Iterable[Tuple[Country, int]]:
        if len(self._countries) < 2:
            return ((c, 0) for c in self._countries)

        days_per_motif = (
            self._simulate_country(i)
            for i in range(len(self._countries))
        )

        aggregator = lambda x, y: map(max, zip(x, y))
        aggregated_days = reduce(aggregator, days_per_motif)
        result = zip(self._countries, aggregated_days)

        return sorted(result, key=lambda x: (x[1], x[0].name))

    def _simulate_country(self, country_index):
        queue: List[City] = []
        for i, country in enumerate(self._countries):
            initial_balance = 0
            is_current = (i == country_index)
            if is_current:
                initial_balance = self._FULL_INITIAL_BALANCE
                queue = country.cities.copy()
            country.init(initial_balance, completion_state=is_current)

        day = 0
        while True:
            new_cities = []
            day += 1
            for city in queue:
                representative_portion = city.balance // self._REPRESENTATIVE_FACTOR
                if representative_portion == 0:
                    continue
                for x, y in self._get_neighbours(city.x, city.y):
                    neighbour: City = self._field[x, y]
                    if neighbour is None:
                        continue
                    if neighbour.is_empty:
                        new_cities.append(neighbour)
                        neighbour.country.add_complete_city(day)
                    city.add_income(-representative_portion)
                    neighbour.add_income(representative_portion)
            queue += new_cities
            for city in queue:
                city.update_balance()

            if self._city_count == len(queue):
                break
        return [c.completion_day for c in self._countries]

    def _get_neighbours(self, x, y):
        # Left
        if x > 0:
            yield x - 1, y
        # Right
        if (x + 1) < self._field.rows:
            yield x + 1, y
        # Up
        if y > 0:
            yield x, y - 1
        # Down
        if (y + 1) < self._field.columns:
            yield x, y + 1
