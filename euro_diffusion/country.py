from euro_diffusion.point import Point
from euro_diffusion.city import City


class Country:
    def __init__(self, name, xl, yl, xh, yh) -> None:
        self.name = name
        self.cities = [
            City(self, x, y)
            for y in range(yl, yh + 1)
            for x in range(xl, xh + 1)
        ]
        self.bottom_left = Point(xl, yl)
        self.top_right = Point(xh, yh)
