from collections import defaultdict
from collections.abc import Sequence


def parse_inputs(lines: Sequence[str]) -> tuple[set[str], list[str]]:
    towels = {towel.strip() for towel in lines[0].rstrip("\n").split(",")}
    designs: list[str] = []
    for i_line, line in enumerate(lines):
        if i_line < 2:
            continue
        else:
            designs.append(line.rstrip("\n"))
    return towels, designs


def parse_one_design(towels: set[str], design: str) -> int:
    arrangements: dict[str, int] = {"": 1}
    updated_arrangements: dict[str, int]
    finished = False
    #
    while not finished:
        updated_arrangements = defaultdict(int)
        for beginning, count in arrangements.items():
            if beginning == design:
                updated_arrangements[beginning] += count
                continue
            remainder = design[len(beginning) :]
            for towel in towels:
                if remainder.startswith(towel):
                    new_beginning = beginning + towel
                    updated_arrangements[new_beginning] += count
        arrangements = updated_arrangements
        finished = all(beginning == design for beginning in arrangements)

    return sum(arrangements.values())


def solve_both_parts(towels: set[str], designs: list[str]) -> tuple[int, int]:
    res_part_1 = 0
    res_part_2 = 0
    for i_design, design in enumerate(designs):
        n_combinations = parse_one_design(towels, design)
        # print(f"{i_design=} {n_combinations=} ({design!r})")
        res_part_1 += n_combinations > 0
        res_part_2 += n_combinations
    return res_part_1, res_part_2


def solve_part_2() -> int:
    return 0


if __name__ == "__main__":
    with open("./inputs/day19/input.txt") as f:
        lines = f.readlines()
    towels, designs = parse_inputs(lines)
    res_part_1, res_part_2 = solve_both_parts(towels, designs)
    print(f"{res_part_1=}")
    print(f"{res_part_2=}")
