import itertools
from collections.abc import Iterable

TYPE_PARSED = list[tuple[int, list[int]]]


def parse_inputs(lines: Iterable[str]) -> TYPE_PARSED:
    eqs = []
    for line in lines:
        line = line.rstrip()
        left, right = line.split(":")
        numbers = [int(i) for i in right.lstrip(" ").split(" ")]
        eqs.append((int(left), numbers))
    return eqs


def parse_one_eq(res: int, numbers: list[int]) -> bool:
    n = len(numbers) - 1
    n_comb = 2**n
    for comb in range(n_comb):
        comb_bin = bin(comb)[2:].rjust(n, "0")
        total = numbers[0]
        for i_op, op in enumerate(comb_bin):
            if op == "0":
                total += numbers[i_op + 1]
            else:
                total *= numbers[i_op + 1]
            if total > res:
                break
        if res == total:
            a = f"{numbers[0]}"
            for i, c in enumerate(comb_bin.replace("0", "+").replace("1", "*")):
                a = f"({a} {c} {numbers[i+1]})"
            return True
    return False


def parse_one_eq_part2(res: int, numbers: list[int]) -> bool:
    if parse_one_eq(res, numbers):
        return True
    n = len(numbers) - 1
    for comb in itertools.product(["+", "*", ""], repeat=n):
        total = numbers[0]
        for i_op, op in enumerate(comb):
            if op == "+":
                total += numbers[i_op + 1]
            elif op == "*":
                total *= numbers[i_op + 1]
            elif op == "":
                total = int(str(total) + str(numbers[i_op + 1]))
            else:
                raise ValueError()
        if res == total:
            return True

    return False


def solve_part_1(eqs: TYPE_PARSED) -> int:
    total = 0
    for left, numbers in eqs:
        ok = parse_one_eq(left, numbers)
        if ok:
            total += left

    # 1289579147154 : too high
    # 1289579105366
    return total


def solve_part_2(eqs: TYPE_PARSED) -> int:
    total = 0
    for i_eq, (left, numbers) in enumerate(eqs):
        ok = parse_one_eq_part2(left, numbers)
        if ok:
            total += left
    return total


if __name__ == "__main__":
    with open("./inputs/day07/input.txt") as f:
        lines = f.readlines()
    eqs = parse_inputs(lines)
    res_part_1 = solve_part_1(eqs)
    print(f"{res_part_1=}")
    res_part_2 = solve_part_2(eqs)
    print(f"{res_part_2=}")
