def count_safe_tiles(first_row: list[bool], rows: int) -> int:
    row = first_row
    safe = row.count(False)
    for _ in range(1, rows):
        row = [row[1]] + [
            row[i-1] ^ row[i+1]
            for i in range(1, len(row) - 1)
        ] + [row[-2]]
        safe += row.count(False)
    return safe


def read_input(filename: str) -> list[bool]:
    return [c == '^' for c in open(filename).read().strip()]


def part_one(filename: str) -> int:
    return count_safe_tiles(read_input(filename), 40)


def part_two(filename: str) -> int:
    return count_safe_tiles(read_input(filename), 400000)
