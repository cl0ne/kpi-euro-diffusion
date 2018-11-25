import unittest
from euro_diffusion.simulator import Simulator, Country


class SimulatorCase(unittest.TestCase):
    def test_zero_countries(self):
        result = list(Simulator([]).run())
        self.assertEqual(result, [])

    def test_one_country(self):
        c = Country('Luxembourg', 1, 2, 3, 4)
        result = list(Simulator([c]).run())
        self.assertEqual(result, [(c, 0)])

    def test_two_equal_countries(self):
        countries = [
            Country('Netherlands', 1, 3, 2, 4),
            Country('Belgium', 1, 1, 2, 2)
        ]
        expected = [
            (countries[1], 2),
            (countries[0], 2)
        ]
        result = list(Simulator(countries).run())
        self.assertEqual(result, expected)

    def test_three_countries(self):
        countries = [
            Country('France', 1, 4, 4, 6),
            Country('Spain', 3, 1, 6, 3),
            Country('Portugal', 1, 1, 2, 2)
        ]
        expected = [
            (countries[1], 382),
            (countries[2], 416),
            (countries[0], 1325)
        ]
        result = list(Simulator(countries).run())
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
