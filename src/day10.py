from collections.abc import Sequence

TYPE_TOPO = list[list[int]]
TYPE_ZEROS = list[complex]


def parse_inputs(lines: Sequence[str]) -> tuple[TYPE_TOPO, TYPE_ZEROS]:
    topo: TYPE_TOPO = []
    zeros: TYPE_ZEROS = []
    for i_row, line in enumerate(lines):
        line = line.rstrip("\n")
        row = [int(c) for c in list(line)]
        topo.append(row)
        for i_col, col in enumerate(row):
            if col == 0:
                zeros.append(complex(i_col, i_row))
    return topo, zeros


diffs = [
    complex(1, 0),
    complex(0, 1),
    complex(-1, 0),
    complex(0, -1),
]


def parse_one_trailhead(topo: TYPE_TOPO, zero: complex) -> int:
    n_rows = len(topo)
    n_cols = len(topo[0])
    trails = [[zero]]
    for step in range(1, 10):
        new_trails = []
        for trail in trails:
            pos = trail[-1]
            for diff in diffs:
                new_pos = pos + diff
                new_x = int(new_pos.real)
                new_y = int(new_pos.imag)
                if (
                    (0 <= new_x < n_cols)
                    and (0 <= new_y < n_rows)
                    and topo[new_y][new_x] == step
                ):
                    new_trails.append(list(trail) + [new_pos])

        trails = new_trails

    return len(trails)


def solve_part_1(topo: TYPE_TOPO, zeros: TYPE_ZEROS) -> int:
    total = 0
    for i_zero, zero in enumerate(zeros):
        res = parse_one_trailhead(topo, zero)
        print(f"trailhead {i_zero}: {res} trails")
        total += res
    return total


def solve_part_2(topo: TYPE_TOPO, zeros: TYPE_ZEROS) -> int:
    return 0


if __name__ == "__main__":
    with open("./inputs/day10/input.txt") as f:
        lines = f.readlines()
    topo, zeros = parse_inputs(lines)
    res_part_1 = solve_part_1(topo, zeros)
    print(f"{res_part_1=}")
    res_part_2 = solve_part_2(topo, zeros)
    print(f"{res_part_2=}")
