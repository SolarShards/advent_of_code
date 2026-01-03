def read_input(filename: str) -> list[list[int]]:
    return [list(map(int, list(line.strip()))) for line in open(filename)]


def part_one(filename: str) -> int:
    banks = read_input(filename)
    joltage = 0
    for bank in banks:
        tens = max(bank[:-1])
        units = max(bank[bank.index(tens)+1:])
        joltage += tens * 10 + units
    return joltage


def find_twelve_batteries(bank: str):
    indexed_bank = list(enumerate(bank))
    best_digits = []
    lookup_start = 0

    for lookup_end in list(range(-11, 1))[:-1] + [None]:
        roi = indexed_bank[lookup_start:lookup_end]
        best_digit = max(roi, key=lambda t: (t[1], -t[0]))
        best_digits.append(best_digit)
        lookup_start = best_digit[0] + 1

    return int("".join([str(t[1]) for t in sorted(best_digits)]))


def part_two(filename: str) -> int:
    banks = read_input(filename)
    joltage = 0
    for bank in banks:
        joltage += find_twelve_batteries(bank)
    return joltage
