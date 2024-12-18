from collections import defaultdict
from collections.abc import Iterable, Sequence


def parse_inputs(lines: Iterable[str]) -> tuple[list[int], list[int]]:
    lefts = []
    rights = []
    for line in lines:
        lists = line.rstrip("\n").split(" ")
        lefts.append(int(lists[0]))
        rights.append(int(lists[-1]))

    return lefts, rights


def solve_part_1(lefts: Sequence[int], rights: Sequence[int]) -> int:
    lsorted = sorted(lefts)
    rsorted = sorted(rights)
    #
    total = 0
    for i, left in enumerate(lsorted):
        total += abs(left - rsorted[i])

    return total


def solve_part_2(lefts: Sequence[int], rights: Sequence[int]) -> int:
    counts: dict[int, int] = defaultdict(int)
    for i in rights:
        counts[i] += 1

    total = 0
    for left in lefts:
        total += left * counts[left]

    return total


if __name__ == "__main__":
    with open("./inputs/day01/input.txt") as f:
        lines = f.readlines()

    lefts, rights = parse_inputs(lines)
    res_part1 = solve_part_1(lefts, rights)
    print(f"{res_part1=}")
    res_part2 = solve_part_2(lefts, rights)
    print(f"{res_part2=}")
