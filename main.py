#!/usr/bin/env python3

import sys

from euro_diffusion import Country, Simulator


def main(argv):
    f = sys.stdin
    case_number = 1
    while True:
        country_count = int(f.readline())
        if country_count == 0:
            break
        if not(1 <= country_count <= 20):
            print('Country count should be between 1 and 20')
            return 1
        countries = []
        for i in range(country_count):
            name, *coordinates = f.readline().split()
            if len(name) > 25:
                print(f'City "{name}" has name longer than 25 chars')
                return 1
            try:
                xl, yl, xh, yh = map(int, coordinates)
            except ValueError:
                print('City coordinates should be 4 integers')
                return 1
            if not(1 <= xl <= xh <= 10 and 1 <= yl <= yh <= 10):
                print('city', name, 'has coordinates outside of allowed bounds - [1, 10] or in the wrong order')
                return 1
            countries.append(Country(name, xl, yl, xh, yh))
        print('Case Number', case_number)
        for c, d in Simulator(countries).run():
            print(c.name, d)
        case_number += 1
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
