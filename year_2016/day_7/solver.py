import re


def read_input(filename: str) -> list[str]:
    return [line.strip() for line in open(filename)]


def part_one(filename: str) -> int:
    ips = read_input(filename)
    tls_compatible = 0
    abba_pattern = re.compile(r"(.)(?!\1)(.)\2\1")
    for ip in ips:
        parts = re.split(r"\[|\]", ip)
        first_hypernet = ip[0] != '['
        for part in parts[first_hypernet::2]:
            if abba_pattern.search(part):
                break
        else:
            for part in parts[not first_hypernet::2]:
                if abba_pattern.search(part):
                    print(ip)
                    tls_compatible += 1
                    break

    return tls_compatible


def part_two(filename: str) -> int:
    ssl_compatible = 0
    aba_pattern = re.compile(r"(?=(.)(?!\1)(.)\1)")
    for ip in read_input(filename):
        parts = re.split(r"\[|\]", ip)
        first_hypernet = ip[0] != '['
        compatible = False
        for supernet in parts[not first_hypernet::2]:
            if compatible:
                break
            for m in aba_pattern.findall(supernet):
                if compatible:
                    break
                bab = m[1] + m[0] + m[1]
                for hypernet in parts[first_hypernet::2]:
                    if bab in hypernet:
                        compatible = True
                        break
        if compatible:
            ssl_compatible += 1

    return ssl_compatible
