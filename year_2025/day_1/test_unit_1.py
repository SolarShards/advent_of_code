from day_1.solver import Rotation, part_two, add, sub


def test_go_left_to_zero_then_left():
    instructions = [
        Rotation(sub, 50),
        Rotation(sub, 50)
    ]
    assert part_two(instructions) == 1


def test_go_left_to_zero_then_right():
    instructions = [
        Rotation(sub, 50),
        Rotation(add, 50)
    ]
    assert part_two(instructions) == 1


def test_go_right_to_zero_then_left():
    instructions = [
        Rotation(add, 50),
        Rotation(sub, 50)
    ]
    assert part_two(instructions) == 1


def test_go_right_to_zero_then_right():
    instructions = [
        Rotation(add, 50),
        Rotation(add, 50)
    ]
    assert part_two(instructions) == 1


def test_go_left_over_zero():
    instructions = [
        Rotation(sub, 70),
        Rotation(add, 10)
    ]
    assert part_two(instructions) == 1


def test_go_right_over_zero():
    instructions = [
        Rotation(add, 70),
        Rotation(sub, 10)
    ]
    assert part_two(instructions) == 1


def test_two_turns_left():
    instructions = [Rotation(sub, 200)]
    assert part_two(instructions) == 2


def test_two_turns_right():
    instructions = [Rotation(add, 200)]
    assert part_two(instructions) == 2


def test_go_left_over_zero_then_left_to_zero():
    instructions = [Rotation(sub, 150)]
    assert part_two(instructions) == 2


def test_go_left_over_zero_then_right_to_zero():
    instructions = [
        Rotation(sub, 100),
        Rotation(add, 50)
    ]
    assert part_two(instructions) == 2


def test_go_right_over_zero_then_right_to_zero():
    instructions = [Rotation(add, 150)]
    assert part_two(instructions) == 2


def test_go_right_over_zero_then_left_to_zero():
    instructions = [
        Rotation(add, 100),
        Rotation(sub, 50)
    ]
    assert part_two(instructions) == 2
