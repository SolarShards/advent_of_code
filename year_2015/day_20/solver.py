from math import sqrt


def read_input(filename: str) -> int:
    return 33_100_000


def part_one(filename: str) -> int:
    target = read_input('') / 10
    house = presents = 0
    while presents < target:
        house += 1
        presents = 0
        for i in range(1, int(sqrt(house)) + 1):
            if house % i == 0:
                presents += i
                if house // i != i:
                    presents += house // i
    return house


def part_two(filename: str) -> int:
    target = read_input('') / 11
    house = presents = 0
    while presents < target:
        house += 1
        presents = 0
        for i in range(1, int(sqrt(house)) + 1):
            if house % i == 0:
                if house <= i * 50:
                    presents += i
                if house // i != i:
                    if house <= house // i * 50:
                        presents += house // i
    return house
