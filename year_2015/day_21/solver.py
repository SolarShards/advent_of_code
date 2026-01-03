from dataclasses import dataclass
from itertools import combinations
from math import ceil


@dataclass
class Item:
    cost: int
    damage: int
    armor: int


weapons = {
    "Dagger": Item(8, 4, 0),
    "Shortsword": Item(10, 5, 0),
    "Warhammer": Item(25, 6, 0),
    "Longsword": Item(40, 7, 0),
    "Greataxe": Item(74, 8, 0)
}

armors = {
    "Shirt": Item(0, 0, 0),
    "Leather": Item(13, 0, 1),
    "Chainmail": Item(31, 0, 2),
    "Splintmail": Item(53, 0, 3),
    "Bandedmail": Item(75, 0, 4),
    "Platemail": Item(102, 0, 5)
}

rings = {
    "Empty Left": Item(0, 0, 0),
    "Empty Right": Item(0, 0, 0),
    "Damage +1": Item(25, 1, 0),
    "Damage +2": Item(50, 2, 0),
    "Damage +3": Item(100, 3, 0),
    "Defense +1": Item(20, 0, 1),
    "Defense +2": Item(40, 0, 2),
    "Defense +3": Item(80, 0, 3)
}


@dataclass
class Character:
    hp: int
    damage: int
    armor: int

    def beats(self, enemy: 'Character') -> bool:
        turns_to_win = ceil(enemy.hp / max(1, (self.damage - enemy.armor)))
        turns_to_lose = ceil(self.hp / max(1, (enemy.damage - self.armor)))
        return turns_to_win <= turns_to_lose


@dataclass
class Player(Character):
    cost: int = 0

    def equip(self, weapon: Item, armor: Item, l_ring: Item, r_ring: Item):
        self.damage = weapon.damage + l_ring.damage + r_ring.damage
        self.armor = armor.armor + l_ring.armor + r_ring.armor
        self.cost = weapon.cost + armor.cost + l_ring.cost + r_ring.cost


def read_input(filename: str) -> Character:
    return Character(*(int(line.split()[-1]) for line in open(filename)))


def part_one(filename: str) -> int:
    player, boss, cost = Player(100, 0, 0), read_input(filename), 1000
    for weapon in weapons.values():
        for armor in armors.values():
            for left_ring, right_ring in combinations(rings.values(), 2):
                player.equip(weapon, armor, left_ring, right_ring)
                if player.beats(boss) and player.cost < cost:
                    cost = player.cost
    return cost


def part_two(filename: str) -> int:
    player, boss, cost = Player(100, 0, 0), read_input(filename), 0
    for weapon in weapons.values():
        for armor in armors.values():
            for left_ring, right_ring in combinations(rings.values(), 2):
                player.equip(weapon, armor, left_ring, right_ring)
                if not player.beats(boss) and player.cost > cost:
                    cost = player.cost
    return cost
