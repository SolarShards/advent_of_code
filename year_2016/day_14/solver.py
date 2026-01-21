import re
from hashlib import md5


def find_last_key(salt: str, stretching: bool = False) -> int:
    triplets, quintuplets, valid, idx = [], [], 0, 0
    while True:
        h = md5(f"{salt}{idx}".encode()).hexdigest()
        if stretching:
            for _ in range(2016):
                h = md5(h.encode()).hexdigest()
        if (m := re.search(r"(.)\1\1", h)):
            triplets.append((idx, m.group(1)))
        if (m := re.search(r"(.)\1\1\1\1", h)):
            quintuplets.append((idx, m.group(1)))

        if quintuplets and quintuplets[0][0] + 1000 == idx:
            quintuplets.pop(0)

        if triplets and triplets[0][0] + 1000 == idx:
            ti, tc = triplets.pop(0)
            for qi, qc in quintuplets:
                if qc == tc:
                    valid += 1
                    if valid == 64:
                        return ti
                    break
        idx += 1


def read_input(filename: str) -> str:
    return open(filename).read().strip()


def part_one(filename: str) -> int:
    return find_last_key(read_input(filename))


def part_two(filename: str) -> int:
    return find_last_key(read_input(filename), stretching=True)
