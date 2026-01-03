def read_input(
        filename: str
        ) -> tuple[
            dict[int, tuple[tuple[int, int], ...]],
            tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]
            ]:
    input_data = [
        group.split("\n")
        for group in open(filename).read().split("\n\n")
    ]
    shapes = {
        int(shape[0][:-1]): tuple([
            (i, j)
            for i, row in enumerate(shape[1:])
            for j, ch in enumerate(row) if ch == "#"
        ])
        for shape in input_data[:-1]
    }
    regions = tuple([
        (
            tuple(map(int, region[0][:-1].split("x"))),
            tuple(map(int, region[1:]))
        )
        for region in [group.split() for group in input_data[-1]]
    ])

    return shapes, regions


def part_one(filename: str) -> int:
    shapes, regions = read_input(filename)
    count = 0
    for area, presents in regions:
        rounded_area = area[0] * area[1] // 9
        needed_area = sum(presents * 9)
        if rounded_area > needed_area:
            count += 1

    return sum(
        [
            sum(presents * 9) <= area[0] * area[1] // 9 * 9
            for area, presents in regions
        ]
    )


def part_two(filename: str) -> int:
    return 0
