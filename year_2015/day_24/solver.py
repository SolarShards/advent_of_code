from math import prod


def read_input(filename: str) -> list[int]:
    return [int(line.strip()) for line in open(filename)]


def group_packages(packages: list[int], nb_groups: int):
    packages.sort(reverse=True)
    group_weight = sum(packages) // nb_groups
    valid_groups: dict[tuple[int, ...], list[set[int]]] = {}

    for base_weight in packages:

        group = {base_weight}
        for weight in packages:
            if sum(group) + weight <= group_weight:
                group.add(weight)

        if sum(group) == group_weight:
            valid_groups[tuple(group)] = [group]

    for _ in range(nb_groups - 2):
        for first_group in valid_groups.copy():
            extended_groups = []
            for placed_packages in valid_groups[first_group]:

                remaining = list(set(packages) - placed_packages)
                for base_weight in remaining:
                    group = {base_weight}
                    for weight in packages:
                        if sum(group) + weight <= group_weight:
                            group.add(weight)

                    if sum(group) == group_weight:
                        extended_groups.append(group)
                        break

            if extended_groups:
                valid_groups[first_group] = extended_groups
            else:
                del valid_groups[first_group]

    return min([
        prod(group)
        for group in valid_groups
        if len(group) == len(min(valid_groups.keys(), key=len))
    ])


def part_one(filename: str) -> int:
    return group_packages(read_input(filename), 3)


def part_two(filename: str) -> int:
    return group_packages(read_input(filename), 4)
