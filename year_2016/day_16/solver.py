from itertools import batched


def tamper_disk(data: str, size: int) -> str:
    while len(data) < size:
        data += '0' + "".join(["0" if c == "1" else "1" for c in data[::-1]])
    checksum = data[:size]
    while not len(checksum) % 2:
        checksum = "".join(str(int(a == b)) for a, b in batched(checksum, 2))
    return checksum


def read_input(filename: str):
    return open(filename).read().strip()


def part_one(filename: str) -> str:
    return tamper_disk(read_input(filename), 272)


def part_two(filename: str) -> str:
    return tamper_disk(read_input(filename), 35651584)
