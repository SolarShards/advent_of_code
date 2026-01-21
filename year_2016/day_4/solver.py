from string import ascii_lowercase as letters


def read_input(filename: str) -> list[tuple[str, int, str]]:
    return [
        (room[:-11], int(room[-10:-7]), room[-6:-1])
        for room in [line.strip() for line in open(filename)]
    ]


def filter_rooms(
        rooms: list[tuple[str, int, str]]) -> list[tuple[str, int, str]]:
    return [
        (name, sector_id, checksum)
        for name, sector_id, checksum in rooms
        if "".join(
            sorted(
                [letter for letter in letters if letter in name],
                key=lambda letter: name.count(letter),
                reverse=True
            )[:5]
        ) == checksum
    ]


def part_one(filename: str) -> int:
    rooms = filter_rooms(read_input(filename))
    return sum(sector_id for _, sector_id, _ in rooms)


def part_two(filename: str) -> int:
    rooms = filter_rooms(read_input(filename))
    decrypted_rooms = {
        "".join([
            letters[(ord(c) - ord('a') + sector_id) % len(letters)]
            if c in letters else " "
            for c in name
        ]): sector_id
        for name, sector_id, _ in rooms
    }
    return decrypted_rooms["northpole object storage"]
