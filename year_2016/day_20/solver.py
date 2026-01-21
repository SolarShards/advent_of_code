from itertools import pairwise


def combine_ranges(ranges: list[range]):
    combined_ranges = [ranges.pop(0)]
    for r in ranges:
        if r.start > combined_ranges[-1].stop:
            combined_ranges.append(r)
        elif r.stop > combined_ranges[-1].stop:
            combined_ranges[-1] = range(combined_ranges[-1].start, r.stop)
    return combined_ranges


def read_input(filename: str) -> list[range]:
    return [
        range(low, high+1)
        for low, high in sorted(
            tuple(map(int, r.split("-")))
            for r in [line.strip() for line in open(filename)]
        )
    ]


def part_one(filename: str) -> int:
    blacklist = combine_ranges(read_input(filename))
    return 0 if blacklist[0].start > 0 else blacklist[0].stop


def part_two(filename: str) -> int:
    blacklist = combine_ranges(read_input(filename))
    return sum(
        b2.start - b1.stop
        for b1, b2 in pairwise(blacklist)
    ) + (1 << 32) - blacklist[-1].stop


if __name__ == "__main__":
    import os
    print(read_input(os.path.dirname(__file__) + "/input.txt"))
    print(part_one(os.path.dirname(__file__) + "/input.txt"))
    print(part_two(os.path.dirname(__file__) + "/input.txt"))
