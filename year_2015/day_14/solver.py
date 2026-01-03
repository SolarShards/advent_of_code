def read_input(filename: str) -> dict[str, tuple[int, int, int]]:
    return {
        sp[0]: (int(sp[3]), int(sp[6]), int(sp[-2]))
        for sp in [line.split() for line in open(filename)]
    }


def compute_distance(elapsed: int, speed: int, flight: int, rest: int) -> int:
    distance = elapsed // (flight + rest) * speed * flight
    remaindeer = elapsed % (flight + rest)  # Pun of the year
    return distance + (remaindeer if remaindeer <= flight else flight) * speed


def part_one(filename: str) -> int:
    best = 0
    for speed, flight, rest in read_input(filename).values():
        distance = compute_distance(2503, speed, flight, rest)
        if distance > best:
            best = distance
    return best


def part_two(filename: str) -> int:
    charac = read_input(filename)
    scores, positions = {r: 0 for r in charac}, {r: 0 for r in charac}
    for t in range(1, 2504):
        for reindeer, (speed, flight, rest) in charac.items():
            positions[reindeer] = compute_distance(t, speed, flight, rest)
        best = max(positions.values())
        for reindeer in scores:
            if positions[reindeer] == best:
                scores[reindeer] += 1
    return max(scores.values())


if __name__ == "__main__":
    import os
    print(read_input(os.path.dirname(__file__) + "\\input.txt"))
    print(part_one(os.path.dirname(__file__) + "\\input.txt"))
    print(part_two(os.path.dirname(__file__) + "\\input.txt"))
