from dataclasses import dataclass
from typing import Callable, Any
from copy import deepcopy


@dataclass
class Effect:
    duration: int
    on_tick: Callable[['Any'], None] = lambda x: None
    on_clear: Callable[['Any'], None] = lambda x: None

    def tick(self, target: Any):
        self.on_tick(target)
        self.duration -= 1
        if self.duration == 0:
            self.on_clear(target)


def clear_shield(target: 'Player'):
    target.armor = 0


def apply_poison(target: 'Boss'):
    target.hp -= 3


def apply_recharge(target: 'Player'):
    target.mp += 101


@dataclass
class Character:
    hp: int
    effects: dict[str, Effect]


@dataclass
class Player(Character):
    mp: int
    spent_mp: int
    armor: int = 0


@dataclass
class Boss(Character):
    attack_damage: int


@dataclass
class Fight:
    player: Player
    boss: Boss


@dataclass
class Spell:
    cost: int
    action: Callable[[Fight], None]
    reqs: Callable[[Fight], bool] = lambda x: True

    def castable(self, fight: Fight) -> bool:
        return self.cost <= fight.player.mp and self.reqs(fight)

    def cast(self, fight: Fight):
        fight.player.mp -= self.cost
        fight.player.spent_mp += self.cost
        self.action(fight)


def magic_missile(fight: Fight):
    fight.boss.hp -= 4


def drain(fight: Fight):
    fight.player.hp += 2
    fight.boss.hp -= 2


def shield(fight: Fight):
    fight.player.armor = 7
    fight.player.effects["shield"] = Effect(6, on_clear=clear_shield)


def poison(fight: Fight):
    fight.boss.effects["poison"] = Effect(6, on_tick=apply_poison)


def recharge(fight: Fight):
    fight.player.effects["recharge"] = Effect(5, on_tick=apply_recharge)


spellbook = (
    Spell(53, magic_missile),
    Spell(73, drain),
    Spell(113, shield, reqs=lambda x: "shield" not in x.player.effects),
    Spell(173, poison, reqs=lambda x: "poison" not in x.boss.effects),
    Spell(229, recharge, reqs=lambda x: "recharge" not in x.player.effects)
)


def fight_result(fight: Fight) -> int | None:
    if fight.boss.hp <= 0:
        return fight.player.spent_mp
    elif fight.player.hp <= 0 or fight.player.mp <= 0:
        return int(1e9)
    else:
        return None


def apply_effects(fight: Fight):
    for unit in fight.player, fight.boss:
        for effect in list(unit.effects):
            unit.effects[effect].tick(unit)
            if unit.effects[effect].duration == 0:
                del unit.effects[effect]


def simulate_fights(initial_state: Fight, hardmode: bool = False) -> int:
    realities = [initial_state]
    min_spent = int(1e9)
    while realities:
        next_turns = []
        for r in realities:

            if hardmode:
                r.player.hp -= 1
                if (res := fight_result(r)) is not None:
                    min_spent = min(res, min_spent)
                    continue

            apply_effects(r)

            if (res := fight_result(r)) is not None:
                min_spent = min(res, min_spent)
                continue

            for spell in spellbook:
                if not spell.castable(r):
                    continue
                fight = deepcopy(r)
                spell.cast(fight)

                if fight.player.spent_mp >= min_spent:
                    continue

                if (res := fight_result(r)) is not None:
                    min_spent = min(res, min_spent)
                    continue

                apply_effects(fight)

                fight.player.hp -= \
                    fight.boss.attack_damage - fight.player.armor

                if (res := fight_result(r)) is not None:
                    min_spent = min(res, min_spent)
                    continue

                next_turns.append(fight)

        realities = next_turns

    return min_spent
