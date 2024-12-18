from collections.abc import Sequence

import numpy as np
from matplotlib import figure

TYPE_ROBOT = tuple[complex, complex]


def parse_inputs(lines: Sequence[str]) -> list[TYPE_ROBOT]:
    robots: list[TYPE_ROBOT] = []
    #
    for line in lines:
        line = line.rstrip("\n")
        position, velocity = line.split(" ")
        px, py = position.lstrip("p=").split(",")
        vx, vy = velocity.lstrip("v=").split(",")
        pos = complex(int(px), int(py))
        vel = complex(int(vx), int(vy))
        robots.append((pos, vel))
    return robots


def move_one_robot(robot: TYPE_ROBOT, n_rows: int, n_cols: int, n_iter: int) -> complex:
    pos, vel = robot
    new_pos_temp = pos + n_iter * vel
    new_x = int(new_pos_temp.real) % n_cols
    new_y = int(new_pos_temp.imag) % n_rows
    return complex(new_x, new_y)


def solve_part_1(robots: list[TYPE_ROBOT], n_rows: int, n_cols: int) -> int:
    quadrants = {"TL": 0, "TR": 0, "BL": 0, "BR": 0}
    n_iter = 100
    lr_limit = n_cols // 2
    tb_limit = n_rows // 2

    for robot in robots:
        new_pos = move_one_robot(robot, n_rows, n_cols, n_iter)
        x = int(new_pos.real)
        y = int(new_pos.imag)
        #
        if (0 <= x < lr_limit) and (0 <= y < tb_limit):
            quadrants["TL"] += 1
        elif (lr_limit < x < n_cols) and (0 <= y < tb_limit):
            quadrants["TR"] += 1
        elif (0 <= x < lr_limit) and (tb_limit < y < n_rows):
            quadrants["BL"] += 1
        elif (lr_limit < x < n_cols) and (tb_limit < y < n_rows):
            quadrants["BR"] += 1
        else:
            pass
    res = quadrants["TL"] * quadrants["TR"] * quadrants["BL"] * quadrants["BR"]
    return res


def solve_part_2(robots: list[TYPE_ROBOT], n_rows: int, n_cols: int) -> int:
    for i in range(1, 10500):
        if i % 100 == 0:
            print(i)
        # image: list[str] = n_rows * [n_cols*"."]
        image = np.zeros((n_rows, n_cols))
        for robot in robots:
            new_pos = move_one_robot(robot, n_rows, n_cols, i)
            x = int(new_pos.real)
            y = int(new_pos.imag)
            image[y, x] = 1
        # cond = np.all(image == np.flipud(image))
        fig = figure.Figure()
        ax = fig.subplots(1)
        ax.imshow(image, cmap="hot")
        fig.savefig(f"img/day141/iter{i:04d}.png")
        fig.clf()
    return 0


if __name__ == "__main__":
    filename = "input"
    if filename == "input0":
        n_rows = 7
        n_cols = 11
    elif filename == "input":
        n_rows = 103
        n_cols = 101
    with open(f"./inputs/day14/{filename}.txt") as f:
        lines = f.readlines()
    robots = parse_inputs(lines)
    res_part_1 = solve_part_1(robots, n_rows, n_cols)
    print(f"{res_part_1=}")
    res_part_2 = solve_part_2(robots, n_rows, n_cols)
    print(f"{res_part_2=}")
