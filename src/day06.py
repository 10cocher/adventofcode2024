import copy
from collections.abc import Iterable


def parse_inputs(
    lines: Iterable[str],
) -> tuple[set[complex], complex, tuple[int, int]]:
    i_row = 1
    blocks: set[complex] = set()
    for line in lines:
        line = line.rstrip()
        n_cols = len(line)
        for i_col, c in enumerate(line):
            if c == "#":
                blocks.add(complex(i_col, i_row))
            elif c == "^":
                pos = complex(i_col, i_row)
        i_row += 1
    n_rows = i_row - 1
    return blocks, pos, (n_rows, n_cols)


def solve_part_1(
    blocks: set[complex], pos_initial: complex, n_rows: int, n_cols: int
) -> tuple[int, set[complex]]:
    pos = pos_initial
    #
    direction = complex(0, -1)
    #
    marked: set[complex] = set()
    #
    while (0 <= int(pos.real) < n_cols) and (1 <= int(pos.imag) <= n_rows):
        marked.add(pos)
        pos0 = pos + direction
        if pos0 in blocks:
            direction *= complex(0, 1)
            pos = pos + direction
        else:
            pos = pos0

    return len(marked), marked


def solve_part_2(
    blocks_initial: set[complex],
    pos_initial: complex,
    n_rows: int,
    n_cols: int,
    marked: set[complex],
) -> int:
    candidates = copy.deepcopy(marked)
    candidates.remove(pos_initial)
    n_candidates = len(candidates)
    #
    count = 0
    #
    for i_candidate, candidate in enumerate(candidates):
        print(f"{i_candidate:4}/{n_candidates}")
        path: set[tuple[complex, complex]] = set()
        blocks = copy.deepcopy(blocks_initial)
        blocks.add(candidate)
        pos = copy.deepcopy(pos_initial)
        direction = complex(0, -1)
        #
        while (0 <= int(pos.real) < n_cols) and (1 <= int(pos.imag) <= n_rows):
            path.add((pos, direction))
            pos0 = pos + direction
            while pos0 in blocks:
                direction *= complex(0, 1)
                pos0 = pos + direction
            pos = pos0
            if (pos, direction) in path:
                count += 1
                break

    return count


if __name__ == "__main__":
    with open("./inputs/day06/input.txt") as f:
        lines = f.readlines()
    blocks, pos, (n_rows, n_cols) = parse_inputs(lines)
    res_part_1, marked = solve_part_1(blocks, pos, n_rows, n_cols)
    print(f"{res_part_1=}")
    res_part_2 = solve_part_2(blocks, pos, n_rows, n_cols, marked)
    print(f"{res_part_2=}")
