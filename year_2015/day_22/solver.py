from game import Player, Boss, Fight, simulate_fights


def read_input(filename: str) -> Boss:
    hp, damage = (int(line.split()[-1]) for line in open(filename))
    return Boss(hp, {}, damage)


def part_one(filename: str) -> int:
    return simulate_fights(
        Fight(Player(50, {}, 500, 0), read_input(filename)),
        hardmode=False
    )


def part_two(filename: str) -> int:
    return simulate_fights(
        Fight(Player(50, {}, 500, 0), read_input(filename)),
        hardmode=True
    )
