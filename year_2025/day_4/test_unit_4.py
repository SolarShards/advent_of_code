from day_4.solver import find_rolls, count_accessible_rolls, remove_accessible_rolls # noqa

plan = [
    list(map(int, line.strip().replace("@", "1").replace(".", "0")))
    for line in [
        "..@@.@@@@.",
        "@@@.@.@.@@",
        "@@@@@.@.@@",
        "@.@@@@..@.",
        "@@.@@@@.@@",
        ".@@@@@@@.@",
        ".@.@.@.@@@",
        "@.@@@.@@@@",
        ".@@@@@@@@.",
        "@.@.@@@.@."
    ]
]


def test_example_1():
    rolls = find_rolls(plan)
    assert count_accessible_rolls(plan, rolls) == 13


def test_example_2():
    rolls = find_rolls(plan)
    assert remove_accessible_rolls(plan, rolls) == 43
