#!/usr/bin/env python3

import sys

from euro_diffusion import Country, Simulator


def main(argv):
    countries = [
        Country('France', 1, 4, 4, 6),
        Country('Spain', 3, 1, 6, 3),
        Country('Portugal', 1, 1, 2, 2)
    ]
    for c, d in Simulator(countries).run():
        print(c.name, ':', d)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
