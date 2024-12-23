import itertools
from collections import defaultdict
from collections.abc import Sequence


def parse_inputs(lines: Sequence[str]) -> list[tuple[str, str]]:
    links: list[tuple[str, str]] = []
    for line in lines:
        a, b = line.rstrip("\n").split("-")
        links.append((a, b))
    return links


def solve_part_1(mapping: dict[str, set[str]]) -> int:
    valid_groups: set[str] = set()
    non_valid_groups: set[str] = set()

    for computer, neighbours in mapping.items():
        for n1, n2 in itertools.combinations(neighbours, 2):
            group = ",".join(sorted({computer, n1, n2}))
            if (group in valid_groups) or (group in non_valid_groups):
                continue
            if n2 in mapping[n1]:
                valid_groups.add(group)
            else:
                non_valid_groups.add(group)

    counter = 0
    for group in valid_groups:
        a, b, c = group.split(",")
        if a.startswith("t") or b.startswith("t") or c.startswith("t"):
            counter += 1

    return counter


def solve_part_2(mapping: dict[str, set[str]]) -> str:
    valid_groups: set[str] = set()
    non_valid_groups: set[str] = set()
    largest_size = 3
    for computer, neighbours in mapping.items():
        for neighbours_size in range(largest_size - 1, len(neighbours) + 1):
            for sub_group in itertools.combinations(neighbours, neighbours_size):
                group = {computer}
                group.update(set(sub_group))
                group_str = ",".join(sorted(group))
                if (group_str in valid_groups) or (group_str in non_valid_groups):
                    continue
                ok = all(
                    n2 in mapping[n1] for n1, n2 in itertools.combinations(sub_group, 2)
                )
                if ok:
                    valid_groups.add(group_str)
                    largest_size = max(largest_size, len(group))
                else:
                    non_valid_groups.add(group_str)

    largest_groups = [
        group for group in valid_groups if len(group.split(",")) == largest_size
    ]

    return largest_groups[0]


if __name__ == "__main__":
    with open("./inputs/day23/input.txt") as f:
        lines = f.readlines()
    links = parse_inputs(lines)
    #
    mapping: dict[str, set[str]] = defaultdict(set)
    for a, b in links:
        mapping[a].add(b)
        mapping[b].add(a)
    #
    res_part_1 = solve_part_1(mapping)
    print(f"{res_part_1=}")
    res_part_2 = solve_part_2(mapping)
    print(f"{res_part_2=}")
