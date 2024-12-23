from collections.abc import Iterable, Sequence


def parse_inputs(
    lines: Sequence[str],
) -> tuple[complex, set[complex], list[complex], str]:
    walls: set[complex] = set()
    boxes: list[complex] = []
    robot_pos: complex
    moves: str = ""
    #
    parse_board: bool = True
    for i_row, line in enumerate(lines):
        line = line.strip("\n")
        if not line:
            parse_board = False
            continue
        if parse_board:
            for i_col, char in enumerate(line):
                coord = complex(i_col, i_row)
                if char == "#":
                    walls.add(coord)
                elif char == "O":
                    boxes.append(coord)
                elif char == "@":
                    robot_pos = coord
        else:
            moves += line

    return robot_pos, walls, boxes, moves


def print_board(
    robot_pos: complex,
    walls: Iterable[complex],
    boxes: Iterable[complex],
    part1: bool = True,
) -> None:
    n_rows = max(int(wall.imag) for wall in walls) + 1
    n_cols = max(int(wall.real) for wall in walls) + 1
    #
    board: list[list[str]] = []
    for i_row in range(n_rows):
        board.append(n_cols * ["."])
    for wall in walls:
        x = int(wall.real)
        y = int(wall.imag)
        board[y][x] = "#"
    for box in boxes:
        x = int(box.real)
        y = int(box.imag)
        if part1:
            board[y][x] = "O"
        else:
            board[y][x] = "["
            board[y][x + 1] = "]"
    #
    x = int(robot_pos.real)
    y = int(robot_pos.imag)
    board[y][x] = "@"
    for row in board:
        print("".join(row))
    return


move_to_diff = {
    ">": complex(1, 0),
    "v": complex(0, 1),
    "<": complex(-1, 0),
    "^": complex(0, -1),
}


def one_move(
    robot_pos: complex,
    boxes: list[complex],
    walls: set[complex],
    move: str,
) -> tuple[complex, list[complex]]:
    ok_move = False
    boxes_index_to_move: set[int] = set()
    #
    diff = move_to_diff[move]
    new_pos = robot_pos + diff
    while new_pos not in walls:
        if new_pos in boxes:
            i_box = boxes.index(new_pos)
            boxes_index_to_move.add(i_box)
            new_pos += diff
        else:
            ok_move = True
            break
    #
    if ok_move:
        robot_pos += diff
        for i_box in boxes_index_to_move:
            boxes[i_box] += diff
    return robot_pos, boxes


def transform_board(
    robot_pos: complex, walls: Iterable[complex], boxes: Iterable[complex]
) -> tuple[complex, set[complex], list[complex]]:
    #
    x = int(robot_pos.real)
    y = int(robot_pos.imag)
    new_robot_pos = complex(2 * x, y)
    #
    new_walls: set[complex] = set()
    for wall in walls:
        x = int(wall.real)
        y = int(wall.imag)
        new_walls.add(complex(2 * x, y))
        new_walls.add(complex(2 * x + 1, y))
    #
    new_boxes: list[complex] = []
    for box in boxes:
        x = int(box.real)
        y = int(box.imag)
        new_boxes.append(complex(2 * x, y))
    return new_robot_pos, new_walls, new_boxes


def solve_part_1(
    robot_initial_pos: complex,
    boxes_initial: list[complex],
    walls: set[complex],
    moves: str,
) -> int:
    robot_pos: complex = robot_initial_pos
    boxes: list[complex] = list(boxes_initial)
    #
    # Simulate the robot movements
    # n_moves = len(moves)
    for i_move, move in enumerate(moves):
        # print("~~~~~~~~~~~~~~~~")
        # print(f">>> move {i_move+1}/{n_moves}: {move!r}")
        robot_pos, boxes = one_move(robot_pos, boxes, walls, move)
    # print_board(robot_pos, walls, boxes)
    #
    # Compte the sum of the GPS coordinates
    total: int = 0
    for box in boxes:
        x_box = int(box.real)
        y_box = int(box.imag)
        score = x_box + 100 * y_box
        total += score
    return total


def solve_part_2(
    robot_initial_pos: complex,
    boxes_initial: list[complex],
    walls: set[complex],
    moves: str,
) -> int:
    return 0


if __name__ == "__main__":
    with open("./inputs/day15/input2.txt") as f:
        lines = f.readlines()
    robot_pos, walls, boxes, moves = parse_inputs(lines)
    print_board(robot_pos, walls, boxes, part1=True)
    res_part_1 = solve_part_1(robot_pos, boxes, walls, moves)
    print(f"{res_part_1=}")
    new_robot_pos, new_walls, new_boxes = transform_board(robot_pos, walls, boxes)
    print_board(new_robot_pos, new_walls, new_boxes, part1=False)
    res_part_2 = solve_part_2(new_robot_pos, new_boxes, new_walls, moves)
    print(f"{res_part_2=}")
