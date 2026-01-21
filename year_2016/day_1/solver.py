direction_map = (
    lambda x, y, d: (x, y + d),
    lambda x, y, d: (x + d, y),
    lambda x, y, d: (x, y - d),
    lambda x, y, d: (x - d, y)
)


def read_input(filename: str) -> list[tuple[int, int]]:
    rotation_map = {"L": -1, "R": +1}
    return [
        (rotation_map[move[0]], int(move[1:]))
        for move in open(filename).read().strip().split(", ")
    ]


def part_one(filename: str) -> int:
    x, y, direction = 0, 0, 0
    for rotation, distance in read_input(filename):
        direction = (direction + rotation) % len(direction_map)
        x, y = direction_map[direction](x, y, distance)
    return abs(x) + abs(y)


def part_two(filename: str) -> int:
    cur_x, cur_y, direction = 0, 0, 0
    visited: set[tuple[int, int]] = {(cur_x, cur_y)}
    for rotation, distance in read_input(filename):
        direction = (direction + rotation) % len(direction_map)
        new_x, new_y = direction_map[direction](cur_x, cur_y, distance)
        inc = direction < 2
        if direction % 2:
            for x in range(min(cur_x, new_x) + inc, max(cur_x, new_x) + inc):
                if (x, new_y) in visited:
                    return abs(x) + abs(new_y)
                visited.add((x, new_y))
        else:
            for y in range(min(cur_y, new_y) + inc, max(cur_y, new_y) + inc):
                if (new_x, y) in visited:
                    return abs(new_x) + abs(y)
                visited.add((new_x, y))
        cur_x, cur_y = new_x, new_y
    return 0
