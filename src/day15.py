from collections.abc import Sequence


def parse_inputs(lines: Sequence[str]) -> list[complex]:
    return []


def solve_part_1() -> int:
    return 0


def solve_part_2() -> int:
    return 0


if __name__ == "__main__":
    with open("./inputs/day15/input0.txt") as f:
        lines = f.readlines()
    data = parse_inputs(lines)
    res_part_1 = solve_part_1()
    print(f"{res_part_1=}")
    res_part_2 = solve_part_2()
    print(f"{res_part_2=}")
