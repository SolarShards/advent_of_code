def read_input(filename: str) -> list[tuple[int, int]]:
    return [
        tuple(map(int, ranges.split("-")))
        for ranges in open(filename).read().split(",")
    ]


def part_one(filename: str) -> int:
    ranges = read_input(filename)
    count = 0
    for bounds in ranges:
        for i in range(bounds[0], bounds[1]+1):
            string = str(i)
            if len(string) % 2:
                continue

            half = int(len(string) / 2)
            if string[:half] == string[half:]:
                count += i

    return count


def part_two(filename: str) -> int:
    ranges = read_input(filename)
    count = 0
    compute_divisors = \
        lambda x: [d for d in range(1, x // 2 + 1) if not x % d] # noqa

    for bounds in ranges:
        nb_digits = len(str(bounds[0]))
        divisors = compute_divisors(nb_digits)

        for i in range(bounds[0], bounds[1]+1):
            string = str(i)

            if len(string) != nb_digits:
                nb_digits = len(string)
                divisors = compute_divisors(nb_digits)

            for div in divisors:
                if not "".join(string.split(string[:div])):
                    count += i
                    break

    return count
