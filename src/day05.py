import itertools
from collections import defaultdict
from collections.abc import Iterable


def parse_inputs(
    lines: Iterable[str],
) -> tuple[list[str], list[list[str]]]:
    is_rule = True

    rules: list[str] = []
    updates: list[list[str]] = []

    for line in lines:
        line = line.rstrip("\n")
        if not line:
            is_rule = False
            continue
        if is_rule:
            left, right = line.split("|")
            rules.append(line)
        else:
            updates.append(line.split(","))

    return rules, updates


def select_and_flatten_rules(
    rules: list[str], numbers: list[int]
) -> dict[int, list[int]]:
    a: dict[int, list[int]] = defaultdict(list)
    #
    for rule in rules:
        left, right = rule.split("|")
        ll = int(left)
        r = int(right)
        if (ll in numbers) and (r in numbers):
            a[ll].append(r)

    return a


def get_order(a: dict[int, list[int]], numbers: list[int]) -> list[int]:
    order = []
    remaining = list(numbers)
    while len(remaining) > 1:
        values = set(itertools.chain.from_iterable(a.values()))
        lefts = set(remaining) - values
        if len(lefts) > 1:
            raise ValueError("More than one order possible given the list of rules")
        left = list(lefts)[0]
        order.append(left)
        remaining.remove(left)
        a.pop(left)

    order.append(remaining[0])

    return order


def is_ok_one_update(update: list[str], rules: list[str]) -> bool:
    """Part 1: process one line"""
    n = len(update)
    for i in range(n - 1):
        for j in range(i, n):
            if "|".join([update[j], update[i]]) in rules:
                return False
    return True


def process_one_update(update: list[str], rules: list[str]) -> int:
    """Part 2: process one line"""
    numbers = [int(u) for u in update]
    better_rules = select_and_flatten_rules(rules, numbers)
    order = get_order(better_rules, numbers)
    index = len(order) // 2
    return order[index]


def solve_part_1(rules: list[str], updates: list[list[str]]) -> int:
    count = 0
    for update in updates:
        res = is_ok_one_update(update, rules)
        assert len(update) % 2 == 1
        if res:
            index = len(update) // 2
            count += int(update[index])
    return count


def solve_part_2(rules: list[str], updates: list[list[str]]) -> int:
    count = 0
    for update in updates:
        res = is_ok_one_update(update, rules)
        if res:
            continue
        res2 = process_one_update(update, rules)
        count += res2
    return count


if __name__ == "__main__":
    with open("./inputs/day05/input.txt") as f:
        lines = f.readlines()
    rules, updates = parse_inputs(lines)
    res_part_1 = solve_part_1(rules, updates)
    print(f"{res_part_1=}")
    res_part_2 = solve_part_2(rules, updates)
    print(f"{res_part_2=}")
