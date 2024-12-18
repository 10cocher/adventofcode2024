from collections.abc import Iterable


def parse_inputs(
    lines: Iterable[str],
) -> tuple[list[str], list[str], list[str], list[str]]:
    horizontal: list[str] = [line.rstrip("\n") for line in lines]
    n_rows = len(horizontal)
    n_cols = len(horizontal[0])
    print(f"{n_rows=} {n_cols=}")
    #
    vertical: list[str] = n_cols * [""]
    for i_row in range(n_rows):
        for i_col in range(n_cols):
            vertical[i_col] += horizontal[i_row][i_col]
    #
    diag1: list[str] = (n_rows + n_cols - 1) * [""]
    for i_col in range(n_cols):
        for i_row in range(i_col, n_rows + i_col):
            diag1[i_row] += horizontal[i_row - i_col][i_col]
    #
    diag2: list[str] = (n_rows + n_cols - 1) * [""]
    for i_col in range(n_cols - 1, -1, -1):
        for i_row in range(i_col, n_rows + i_col):
            diag2[i_row] += horizontal[i_row - i_col][n_cols - 1 - i_col]
    #
    return horizontal, vertical, diag1, diag2


def process_one_table(lines: list[str], pattern: str) -> int:
    count1 = 0
    count2 = 0
    for line in lines:
        # print(line)
        #
        start = 0
        while (index := line.find(pattern, start)) >= 0:
            count1 += 1
            start = index + len(pattern)
        #
        start = 0
        while (index := line.find(pattern[::-1], start)) >= 0:
            count2 += 1
            start = index + len(pattern)
    print(f"{count1=}, {count2=}")
    return count1 + count2


def solve_part_1(tabs: list[list[str]]) -> int:
    pattern = "XMAS"
    count = 0
    for tab in tabs:
        count += process_one_table(tab, pattern)
        # break
    return count


def solve_part_2(tab: list[str]) -> int:
    n_rows = len(tab)
    n_cols = len(tab[0])
    print(f"{n_rows=} {n_cols=}")
    count = 0
    for i_row in range(1, n_rows - 1):
        # print(f"{i_row=}", tab[i_row])
        start = 1
        index = tab[i_row].find("A", start)
        while 1 <= index <= n_cols - 2:
            # print(index)
            a = tab[i_row - 1][index - 1] + tab[i_row + 1][index + 1]
            b = tab[i_row + 1][index - 1] + tab[i_row - 1][index + 1]
            if (a in ["MS", "SM"]) and (b in ["MS", "SM"]):
                # print("=====")
                # print(i_row, index)
                # print(tab[i_row-1][index-1] + '.' + tab[i_row-1][index+1])
                # print("...")
                # print(tab[i_row+1][index-1] + '.' + tab[i_row+1][index+1])

                count += 1
            start = index + 1
            index = tab[i_row].find("A", start)

    return count


if __name__ == "__main__":
    with open("./inputs/day04/input.txt") as f:
        lines = f.readlines()
    h, v, d1, d2 = parse_inputs(lines)
    res_part_1 = solve_part_1([h, v, d1, d2])
    print(f"{res_part_1=}")
    res_part_2 = solve_part_2(h)
    print(f"{res_part_2=}")
