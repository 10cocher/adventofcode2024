from collections.abc import Sequence


def parse_inputs(lines: Sequence[str]) -> tuple[dict[str, int], list[int]]:
    for line in lines:
        line = line.rstrip("\n")
        if line.startswith("Register A"):
            a = int(line.lstrip("Register A:"))
        elif line.startswith("Register B"):
            b = int(line.lstrip("Register B:"))
        elif line.startswith("Register C"):
            c = int(line.lstrip("Register C:"))
        elif line.startswith("Program"):
            numbers = [int(i) for i in line.lstrip("Program :").split(",")]

    register = {"A": a, "B": b, "C": c}
    print(register)
    print(numbers)
    return register, numbers


def solve_part_1(register: dict[str, int], numbers: list[int]) -> int:
    return 0


def solve_part_2() -> int:
    return 0


if __name__ == "__main__":
    with open("./inputs/day17/input.txt") as f:
        lines = f.readlines()
    register, numbers = parse_inputs(lines)
    res_part_1 = solve_part_1(register, numbers)
    print(f"{res_part_1=}")
    res_part_2 = solve_part_2()
    print(f"{res_part_2=}")
