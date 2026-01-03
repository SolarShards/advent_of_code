from itertools import combinations_with_replacement
from math import prod


def read_input(
        filename: str
        ) -> dict[str, tuple[int, int, int, int, int]]:
    return {
        sp[0][:-1]: (int(sp[2][:-1]), int(sp[4][:-1]),
                     int(sp[6][:-1]), int(sp[8][:-1]), int(sp[-1]))
        for sp in [line.split() for line in open(filename)]
    }


def compute_recipes(
        stock: dict[str, tuple[int, int, int, int, int]]
        ) -> list[tuple[int, int, int, int, int]]:
    recipes = []
    for comb in combinations_with_replacement(stock.keys(), 100):
        properties = [
            sum(comb.count(ing) * props[i] for ing, props in stock.items())
            for i in range(5)
        ]
        if min(properties[:-1]) > 0:
            recipes.append(properties)
    return recipes


def part_one(filename: str) -> int:
    recipes = compute_recipes(read_input(filename))
    return max(prod(props[:-1]) for props in recipes)


def part_two(filename: str) -> int:
    recipes = compute_recipes(read_input(filename))
    return max(prod(props[:-1]) for props in recipes if props[-1] == 500)
