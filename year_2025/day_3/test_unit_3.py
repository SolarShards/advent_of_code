from day_3.solver import find_twelve_batteries


def test_case_987654321111111():
    bank = list(map(int, list("987654321111111")))
    assert find_twelve_batteries(bank) == 987654321111


def test_case_811111111111119():
    bank = list(map(int, list("811111111111119")))
    assert find_twelve_batteries(bank) == 811111111119


def test_case_234234234234278():
    bank = list(map(int, list("234234234234278")))
    assert find_twelve_batteries(bank) == 434234234278


def test_case_818181911112111():
    bank = list(map(int, list("818181911112111")))
    assert find_twelve_batteries(bank) == 888911112111
