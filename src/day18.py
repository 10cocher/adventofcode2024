from collections.abc import Sequence


def parse_inputs(lines: Sequence[str]) -> list[complex]:
    blocks: list[complex] = []
    #
    for line in lines:
        x, y = line.rstrip("\n").split(",")
        blocks.append(complex(int(x), int(y)))
    return blocks


diffs = [complex(1, 0), complex(0, 1), complex(-1, 0), complex(0, -1)]


def print_path(path: list[complex], blocks: list[complex], n: int) -> None:
    for i_row in range(n + 1):
        row = (n + 1) * ["."]
        # print(row)
        marks = [int(x.real) for x in path if int(x.imag) == i_row]
        # print(marks)
        for m in marks:
            row[m] = "O"
        blocks_row = [int(x.real) for x in blocks if int(x.imag) == i_row]
        # print(blocks_row)
        for b in blocks_row:
            row[b] = "#"
        print("".join(row))
    return


def solve_part_1(
    blocks: list[complex], n: int, n_blocks: int
) -> tuple[int, list[complex]]:
    b = blocks[0:n_blocks]
    start_position = complex(0, 0)
    #
    paths: list[list[complex]] = [[start_position]]
    new_paths: list[list[complex]]
    all_visited_positions = {start_position}
    #
    ok = True
    steps = 0
    while ok:
        steps += 1
        new_paths = []
        if len(paths) < 1:
            print("no way")
            raise ValueError()
        for path in paths:
            last_pos = path[-1]
            all_visited_positions
            for diff in diffs:
                new_pos = last_pos + diff
                new_x = int(new_pos.real)
                new_y = int(new_pos.imag)
                inside_limits = (0 <= new_x <= n) and (0 <= new_y <= n)
                if not inside_limits or new_pos in b:
                    continue
                elif new_pos in path:
                    # do not loop
                    continue
                elif new_pos in all_visited_positions:
                    # there is already a path shorter (or as long as this one) leading
                    # to this new position
                    continue
                else:
                    new_path = list(path) + [new_pos]
                    new_paths.append(new_path)
                    all_visited_positions.add(new_pos)
                    if (new_x == n) and (new_y == n):
                        # print_path(new_path, b, n)
                        ok = False
                        break
            if not ok:
                break

        # print(f"After {steps} steps, there are {len(new_paths)} paths")
        paths = new_paths

    return steps, new_path


def solve_part_2(blocks: list[complex], n: int, n_blocks: int) -> str:
    res = "?"
    path: list[complex] = []
    for i in range(n_blocks + 1, len(blocks) + 1):
        print(f"{i=}")
        if (blocks[i] not in path) and (len(path) > 0):
            continue
        try:
            _, path = solve_part_1(blocks, n, i + 1)
        except ValueError:
            blocker = blocks[i]
            x = int(blocker.real)
            y = int(blocker.imag)
            res = ",".join([str(x), str(y)])
            break
    return res


if __name__ == "__main__":
    filename = "input"
    if filename == "input0":
        n = 6
        n_blocks = 12
    elif filename == "input":
        n = 70
        n_blocks = 1024
    with open(f"./inputs/day18/{filename}.txt") as f:
        lines = f.readlines()
    blocks = parse_inputs(lines)
    res_part_1 = solve_part_1(blocks, n, n_blocks)
    print(f"{res_part_1=}")
    res_part_2 = solve_part_2(blocks, n, n_blocks)
    print(f"{res_part_2=}")
