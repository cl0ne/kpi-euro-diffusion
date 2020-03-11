#!/usr/bin/env python3

import sys

from euro_diffusion import Country, Simulator

MIN_COUNTRY_COUNT = 1
MAX_COUNTRY_COUNT = 20
MAX_COUNTRY_NAME_LENGTH = 1
MIN_CITY_POS = 1
MAX_CITY_POS = 10
EXIT_FAIL = 1

def main(argv):
    f = sys.stdin
    case_number = 1
    while True:
        l = f.readline().strip()
        if not l: # allow empty lines
            continue
        try:
            country_count = int(l)
        except ValueError:
            print('The first line of the case number', case_number,
                  'should contain integer - number of countries')
            return EXIT_FAIL
        if country_count == 0:
            break
        if not(MIN_COUNTRY_COUNT <= country_count <= MAX_COUNTRY_COUNT):
            print('Country count should be between',
                  MIN_COUNTRY_COUNT, 'and', MAX_COUNTRY_COUNT)
            return EXIT_FAIL
        countries = []
        for i in range(country_count):
            try:
                name, *coordinates = f.readline().split()
            except ValueError: # line was empty
                print('Each line of the case should contain name',
                      'of the country and its corner city coordinates')
                return EXIT_FAIL
            if len(name) > MAX_COUNTRY_NAME_LENGTH:
                print(f'Country "{name}" has name longer than',
                       MAX_COUNTRY_NAME_LENGTH, 'chars')
                return EXIT_FAIL

            try:
                xl, yl, xh, yh = map(int, coordinates)
            except ValueError:
                print('Country bounds should be 4 integers')
                return EXIT_FAIL

            if not(
                    MIN_CITY_POS <= xl <= xh <= MAX_CITY_POS
                    and MIN_CITY_POS <= yl <= yh <= MAX_CITY_POS
            ):
                bounds_str = '[{}, {}]'.format(MIN_CITY_POS, MAX_CITY_POS)
                print(f'country "{name}"',
                      'has bounds outside of allowed range',
                      bounds_str,
                      'or in the wrong order')
                return EXIT_FAIL

            countries.append(Country(name, xl, yl, xh, yh))
        print('Case Number', case_number)
        for c, d in Simulator(countries).run():
            print(c.name, d)
        case_number += 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
