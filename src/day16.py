from collections.abc import Sequence

TYPE_PATH = list[tuple[complex, complex, int]]


def parse_inputs(lines: Sequence[str]) -> tuple[set[complex], complex, complex]:
    walls: set[complex] = set()
    start: complex
    end: complex
    #
    for i_row, line in enumerate(lines):
        line = line.strip("\n")
        for i_col, char in enumerate(line):
            coord = complex(i_col, i_row)
            if char == "#":
                walls.add(coord)
            elif char == "S":
                start = coord
            elif char == "E":
                end = coord
            else:
                continue

    return walls, start, end


direction_changes: list[tuple[complex, int]] = [
    (complex(1, 0), 1),  # keep the same direction
    (complex(0, 1), 1001),  # turn right
    (complex(0, -1), 1001),  # turn left
]


def solve_part_1(walls: set[complex], start: complex, end: complex) -> tuple[int, int]:
    east = complex(1, 0)
    paths: list[TYPE_PATH] = [[(start, east, 0)]]
    new_paths: list[TYPE_PATH]
    best_scores: dict[tuple[complex, complex], int] = {(start, east): 0}
    #
    i_step = 0
    while any(_path[-1][0] != end for _path in paths):
        i_step += 1
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(f">>>> {i_step=} - {len(paths)} paths")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>")
        new_paths = []
        for path in paths:
            # print("~~~~~~~~~~~~")
            # print(path)
            # print("~~~~~~~~~~~~")
            position, direction, score = path[-1]
            if position == end:
                new_paths.append(path)
                continue
            # print(f"{position=} {direction=} {score=}")
            #
            for dir_change, cost in direction_changes:
                new_direction = dir_change * direction
                new_position = position + new_direction
                new_score = score + cost
                # print(f"{new_position=} {new_direction=} {new_score=}")
                if new_position in walls:
                    # print("WALL")
                    # do not go through the walls
                    continue
                if new_position in [p[0] for p in path]:
                    # print("LOOP")
                    # useless to go back to an already known position
                    continue
                new_path = list(path) + [(new_position, new_direction, new_score)]
                if (new_position, new_direction) in best_scores:
                    # print("NEW1")
                    current_best_score = best_scores[(new_position, new_direction)]
                    if new_score > current_best_score:
                        # this path will not bring anything better
                        continue
                    else:
                        new_paths.append(new_path)
                else:
                    # print("NEW2")
                    best_scores[(new_position, new_direction)] = new_score
                    new_paths.append(new_path)

        print(f"oooooo {len(new_paths)} new_paths")
        # for _path in (new_paths):
        #    print([_p[0] for _p in _path])
        # Do some pruning
        new_paths_2: list[TYPE_PATH] = []
        for path in new_paths:
            ok = True
            for position, direction, score in path:
                if best_scores[(position, direction)] < score:
                    ok = False
                    break
            if ok:
                new_paths_2.append(path)
        print(f"xxxxxxx {len(new_paths_2)} new_paths after pruning")
        # for _path in (new_paths_2):
        #    print([_p[0] for _p in _path])
        paths = new_paths_2
    # for i_path, path in enumerate(paths):
    #    print(f"<<<<<< path {i_path+1} >>>>>>")
    #    for _p in path:
    #        print(_p)
    print(f"{len(paths)} paths at the end")
    minimum = 1001 * len(paths[0])
    for _path in paths:
        cost = _path[-1][2]
        minimum = min(cost, minimum)

    minimum_paths: list[TYPE_PATH] = []
    for _path in paths:
        if _path[-1][2] == minimum:
            minimum_paths.append(_path)
    print(f"{len(minimum_paths)} minimum paths at the end")
    #
    all_visited: set[complex] = set()
    for _path in minimum_paths:
        all_visited.update({_p[0] for _p in _path})

    return minimum, len(all_visited)


def solve_part_2() -> int:
    return 0


if __name__ == "__main__":
    with open("./inputs/day16/input.txt") as f:
        lines = f.readlines()
    walls, start, end = parse_inputs(lines)
    res_part_1, res_part_2 = solve_part_1(walls, start, end)
    print(f"{res_part_1=}")
    print(f"{res_part_2=}")
