from collections import defaultdict
from collections.abc import Iterable

TYPE_PARSED = dict[str, list[complex]]


def parse_inputs(lines: Iterable[str]) -> tuple[TYPE_PARSED, int, int]:
    char_to_pos: TYPE_PARSED = defaultdict(list)
    for i_row, line in enumerate(lines):
        n_cols = len(line.rstrip("\n"))
        for i_col, c in enumerate(line.rstrip("\n")):
            if c != ".":
                char_to_pos[c].append(complex(i_col, i_row + 1))
    n_rows = i_row + 1
    return char_to_pos, n_rows, n_cols


def parse_one_char(positions: list[complex], n_rows: int, n_cols: int) -> set[complex]:
    antinodes: set[complex] = set()
    n = len(positions)
    for i1 in range(n):
        p1 = positions[i1]
        for i2 in range(i1 + 1, n):
            p2 = positions[i2]
            diff = p2 - p1
            c1 = p2 + diff
            c2 = p1 - diff
            for c in [c1, c2]:
                if (0 <= c.real < n_cols) and (1 <= c.imag <= n_rows):
                    # print(p1, p2, c)
                    antinodes.add(c)

    return antinodes


def parse_one_char_part_2(
    positions: list[complex], n_rows: int, n_cols: int
) -> set[complex]:
    antinodes: set[complex] = set()
    n = len(positions)
    for i1 in range(n):
        p1 = positions[i1]
        for i2 in range(i1 + 1, n):
            p2 = positions[i2]
            diff = p2 - p1
            k = 0
            c = p1 + k * diff
            while (0 <= c.real < n_cols) and (1 <= c.imag <= n_rows):
                antinodes.add(c)
                k += 1
                c = p1 + k * diff
            k = -1
            c = p1 + k * diff
            while (0 <= c.real < n_cols) and (1 <= c.imag <= n_rows):
                antinodes.add(c)
                k += -1
                c = p1 + k * diff

    return antinodes


def solve_part_1(char_to_pos: TYPE_PARSED, n_rows: int, n_cols: int) -> int:
    total_antinodes: set[complex] = set()
    for char, positions in char_to_pos.items():
        print(f"=== {char=}")
        antinodes = parse_one_char(positions, n_rows, n_cols)
        total_antinodes = total_antinodes.union(antinodes)

    # print("=====")
    # to_print = []
    # for i_row in range(n_rows):
    #    to_print.append(n_cols*".")
    # for char, positions in char_to_pos.items():
    #    for p in positions:
    #        y=int(p.imag) - 1
    #        x=int(p.real)
    #        to_print[y] = to_print[y][:x] + char + to_print[y][x+1:]
    # for node in total_antinodes:
    #    y=int(node.imag) - 1
    #    x=int(node.real)
    #    to_print[y] = to_print[y][:x] + "#" + to_print[y][x+1:]
    # for row in to_print:
    #    print(row)
    return len(total_antinodes)


def solve_part_2(char_to_pos: TYPE_PARSED, n_rows: int, n_cols: int) -> int:
    total_antinodes: set[complex] = set()
    for char, positions in char_to_pos.items():
        antinodes = parse_one_char_part_2(positions, n_rows, n_cols)
        total_antinodes = total_antinodes.union(antinodes)
    return len(total_antinodes)


if __name__ == "__main__":
    with open("./inputs/day08/input.txt") as f:
        lines = f.readlines()
    char_to_pos, n_rows, n_cols = parse_inputs(lines)
    res_part_1 = solve_part_1(char_to_pos, n_rows, n_cols)
    print(f"{res_part_1=}")
    res_part_2 = solve_part_2(char_to_pos, n_rows, n_cols)
    print(f"{res_part_2=}")
