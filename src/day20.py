from collections import defaultdict
from collections.abc import Sequence


def parse_inputs(
    lines: Sequence[str],
) -> tuple[set[complex], complex, complex]:
    walls: set[complex] = set()
    #
    for i_row, line in enumerate(lines):
        for i_col, char in enumerate(line.rstrip("\n")):
            if char == "#":
                walls.add(complex(i_col, i_row))
            elif char == "S":
                start = complex(i_col, i_row)
            elif char == "E":
                end = complex(i_col, i_row)
    return walls, start, end


diffs = [complex(1, 0), complex(0, 1), complex(-1, 0), complex(0, -1)]


def find_base_path(walls: set[complex], start: complex, end: complex) -> list[complex]:
    path = [start]
    position = path[-1]
    while position != end:
        for diff in diffs:
            new_pos = position + diff
            if (new_pos in path) or (new_pos in walls):
                continue
            else:
                path.append(new_pos)
        position = path[-1]

    return path


# First implementation for part1: faster, but less elegant
# def solve_part_1(path: list[complex]) -> int:
#    bridges: set[tuple[int, int]] = set()
#    for i_position_start, position in enumerate(path):
#        if i_position_start >= len(path) - 3:
#            break
#        for diff1 in diffs:
#            new_pos_1 = position + diff1
#            if new_pos_1 in path:
#                continue
#            else:
#                for diff2 in diffs:
#                    new_pos_2 = new_pos_1 + diff2
#                    try:
#                        i_position_end = path.index(new_pos_2, i_position_start + 2)
#                    except ValueError:
#                        continue
#                    else:
#                        bridges.add((i_position_start, i_position_end))
#    #
#    shortcuts: dict[int, int] = defaultdict(int)
#    for bridge_start, bridge_end in bridges:
#        gain = bridge_end - bridge_start - 2
#        if gain < 1:
#            continue
#        shortcuts[gain] += 1
#    total = 0
#    for gain, count in sorted(shortcuts.items(), reverse=True):
#        # print(f"{gain=} {count=}")
#        if gain >= 100:
#            total += count
#
#    return total


def solve(path: list[complex], max_steps: int, min_gain: int, print_gains: bool) -> int:
    shortcuts: dict[int, int] = defaultdict(int)
    for i_position_start, position_start in enumerate(path):
        for i_position_end in range(i_position_start + min_gain, len(path)):
            position_end = path[i_position_end]
            delta = position_end - position_start
            delta_x = abs(int(delta.real))
            delta_y = abs(int(delta.imag))
            if delta_x + delta_y <= max_steps:
                gain = i_position_end - i_position_start - delta_x - delta_y
                if gain >= min_gain:
                    shortcuts[gain] += 1
    total = 0
    for gain, count in sorted(shortcuts.items(), reverse=False):
        if print_gains:
            print(f"There are {count} cheats that save {gain} picoseconds")
        if gain >= 100:
            total += count
    return total


if __name__ == "__main__":
    filename = "input"
    with open(f"./inputs/day20/{filename}.txt") as f:
        lines = f.readlines()
    if filename == "input0":
        min_gain = 1
        print_gains = True
    elif filename == "input":
        min_gain = 100
        print_gains = False
    walls, start, end = parse_inputs(lines)
    print("Find base path...")
    base_path = find_base_path(walls, start, end)
    print(f"Base path has length {len(base_path)}")
    print("Solve part 1...")
    res_part_1 = solve(
        base_path, max_steps=2, min_gain=min_gain, print_gains=print_gains
    )
    print(f"{res_part_1=}")
    print("Solve part 2...")
    if filename == "input0":
        min_gain = 50
    res_part_2 = solve(
        base_path, max_steps=20, min_gain=min_gain, print_gains=print_gains
    )
    print(f"{res_part_2=}")
