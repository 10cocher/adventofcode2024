from collections import defaultdict
from collections.abc import Sequence


def transform_number(a: int) -> list[int]:
    if a == 0:
        return [1]
    elif len(astr := str(a)) % 2 == 0:
        b = len(astr) // 2
        return [int(astr[:b]), int(astr[b:])]
    else:
        return [2024 * a]


def solve_dummy(numbers_input: Sequence[int], n: int) -> int:
    numbers = list(numbers_input)
    for i in range(n):
        new_list = []
        for number in numbers:
            new_list.extend(transform_number(number))
        numbers = new_list
        print(f"Run {i+1:2}/{n}: {len(numbers):8}")
        # print(f"{len(numbers):8}", numbers)
    return len(numbers)


def solve_economical(numbers_input: Sequence[int], n: int) -> int:
    numbers_count: dict[int, int] = defaultdict(int)
    for number in numbers_input:
        numbers_count[number] += 1
    #
    new_numbers_count: dict[int, int]
    for i in range(n):
        new_numbers_count = defaultdict(int)
        for number, count in numbers_count.items():
            for new_number in transform_number(number):
                new_numbers_count[new_number] += count
        numbers_count = new_numbers_count
        total = sum(numbers_count.values())
        # n_unique_items = len(numbers_count)
        # print(f"Run {i+1:2}/{n}: {total:8} ({n_unique_items=})")
    return total


if __name__ == "__main__":
    with open("./inputs/day11/input.txt") as f:
        lines = f.readlines()
    numbers = [int(i) for i in lines[0].rstrip("\n").split(" ")]
    res_part_1 = solve_economical(numbers, n=25)
    print(f"{res_part_1=}")
    res_part_2 = solve_economical(numbers, n=75)
    print(f"{res_part_2=}")
