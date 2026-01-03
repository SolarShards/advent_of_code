def read_input(filename: str) -> tuple[list[range], set[int]]:
    database = [line.strip() for line in open(filename)]
    split_id = database.index('')
    ranges = [
        range(low, high+1)
        for low, high in sorted(
            [
                tuple(map(int, r.split("-")))
                for r in database[:split_id]
            ]
        )
    ]
    ids = set(map(int, database[split_id+1:]))
    return ranges, ids


def combine_ranges(ranges: list[range]):
    combined_ranges = [ranges.pop(0)]
    for r in ranges:
        if r.start >= combined_ranges[-1].stop:
            combined_ranges.append(r)
        elif r.stop > combined_ranges[-1].stop:
            combined_ranges[-1] = range(combined_ranges[-1].start, r.stop)
    return combined_ranges


def part_one(filename: str) -> int:
    ranges, ids = read_input(filename)
    ranges = combine_ranges(ranges)
    fresh = 0
    for ingredient in ids:
        for r in ranges:
            if ingredient in r:
                fresh += 1
                break
    return fresh


def part_two(filename: str) -> int:
    ranges, _ = read_input(filename)
    ranges = combine_ranges(ranges)
    return sum([len(r) for r in ranges])
