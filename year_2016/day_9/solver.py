import re


def read_input(filename: str) -> str:
    return open(filename).read().strip()


def part_one(filename: str):
    zipped = read_input(filename)
    unzipped = ""
    while (m := re.search(r"(\((\d+)x(\d+)\))", zipped)) is not None:
        size, rep = map(int, (m.groups()[1:]))
        unzipped += zipped[:m.start()] + zipped[m.end():m.end() + size] * rep
        zipped = zipped[m.end() + size:]
    return len(unzipped + zipped)


def part_two(filename: str) -> int:

    def count_unzipped(data: str) -> int:
        total_size = 0
        while (m := re.search(r"(\((\d+)x(\d+)\))", data)) is not None:
            next_mark = data.find('(')
            if next_mark == -1:
                break
            total_size += next_mark
            size, rep = map(int, (m.groups()[1:]))
            total_size += rep * count_unzipped(data[m.end():m.end() + size])
            data = data[m.end() + size:]
        return total_size + len(data)

    return count_unzipped(read_input(filename))
