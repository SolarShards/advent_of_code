def find_timing(sizes: list[int], positions: list[int]) -> int:
    seconds = max(sizes) - positions[sizes.index(max(sizes))]
    positions = [
        (pos + i+1 + seconds) % sizes[i]
        for i, pos in enumerate(positions)
    ]
    while any(set(positions)):
        positions = [(p+1) % sizes[i] for i, p in enumerate(positions)]
        seconds += 1
    return seconds


def read_input(filename: str) -> tuple[list[int], list[int]]:
    lines = [line.strip()[:-1].split() for line in open(filename)]
    return [int(ln[3]) for ln in lines], [int(ln[-1]) for ln in lines]


def part_one(filename: str) -> int:
    return find_timing(*read_input(filename))


def part_two(filename: str) -> int:
    sizes, positions = read_input(filename)
    sizes.append(11)
    positions.append(0)
    return find_timing(sizes, positions)
