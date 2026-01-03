def read_input(filename: str) -> dict[str, tuple[str, ...]]:
    return {
        devices[0][:-1]: tuple(devices[1:])
        for devices in [line.split() for line in open(filename)]
    }


def count_paths(
        tree: dict[str, tuple[str, ...]],
        start: str,
        target: str) -> int:
    tree["out"] = tuple()
    paths = {device: 0 for device in tree}
    paths[target] = 1
    while True:
        it = {
            device: 1
            if device == target else sum(paths[child] for child in children)
            for device, children in tree.items()
        }
        if it == paths:
            return paths[start]
        paths = it


def part_one(filename: str) -> int:
    return count_paths(read_input(filename), "you", "out")


def part_two(filename: str) -> int:
    dev_list = read_input(filename)

    svr_to_fft = count_paths(dev_list, "svr", "fft")
    fft_to_dac = count_paths(dev_list, "fft", "dac")
    dac_to_out = count_paths(dev_list, "dac", "out")
    m1 = svr_to_fft * fft_to_dac * dac_to_out
    svr_to_dac = count_paths(dev_list, "svr", "dac")
    dac_to_fft = count_paths(dev_list, "dac", "fft")
    fft_to_out = count_paths(dev_list, "fft", "out")
    m2 = svr_to_dac * dac_to_fft * fft_to_out
    return m1 + m2
