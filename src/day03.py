from collections.abc import Iterable


def parse_inputs(lines: Iterable[str]) -> list[str]:
    return [line.rstrip("\n") for line in lines]


def solve_part_1(lines: list[str]) -> int:
    total = 0
    for line in lines:
        # print(f"{line!r}")
        search_start = 0
        while (start := line.find("mul(", search_start)) >= 0:
            # print(f"{search_start=} {start=}")
            comma = line.find(",", start + 4)
            # print(f"{comma=}")
            if comma >= 1:
                end = line.find(")", comma + 1)
                if end >= 1:
                    try:
                        n1 = int(line[start + 4 : comma])
                        n2 = int(line[comma + 1 : end])
                    except ValueError:
                        pass
                    else:
                        # print(f"found {n1=}, {n2=}")
                        total += n1 * n2
            search_start = start + 4

    return total


def solve_part_2(lines: list[str]) -> int:
    total = 0
    total2 = 0
    ok_enabled = True
    for line in lines:
        print("==========================")
        # Find the "do()" and "don't()"
        search_start = 0
        intervals_ok: list[tuple[int, int]] = []
        ok = ok_enabled
        start_ok = 0
        # print(line)
        while (start := line.find("do", search_start)) >= 0:
            # print("=====")
            # print(f"{start=}, {line[start:]}")
            if line[start + 2 : start + 4] == "()":
                if ok:
                    pass
                else:
                    start_ok = start
                    ok = True
            elif line[start + 2 : start + 7] == "n't()":
                if ok:
                    end_ok = start
                    intervals_ok.append((start_ok, end_ok))
                    ok = False
                else:
                    pass
            else:
                print("HUH", line[start : start + 15])

            search_start = start + 2
        if ok:
            intervals_ok.append((start_ok, len(line) + 1))
        ok_enabled = ok
        print(intervals_ok)

        # Find the "mul()"
        # print(f"{line!r}")
        search_start = 0
        while (start := line.find("mul(", search_start)) >= 0:
            # print(f"{search_start=} {start=}")
            comma = line.find(",", start + 4)
            # print(f"{comma=}")
            if comma >= 1:
                end = line.find(")", comma + 1)
                if end >= 1:
                    try:
                        n1 = int(line[start + 4 : comma])
                        n2 = int(line[comma + 1 : end])
                    except ValueError:
                        pass
                    else:
                        # print(f"found {n1=}, {n2=}")
                        ok = any((s <= start <= e for s, e in intervals_ok))
                        if ok:
                            # logger.info(f" ENABLED {start=:5} {n1=:5} {n2=:5}")
                            total += n1 * n2
                        else:
                            total2 += n1 * n2
                            # logger.error(f"DISABLED {start=:5} {n1=:5} {n2=:5}")
            search_start = start + 4

    # 112508982 - too high
    # 62506758 - too low
    print(total, total2, total + total2)

    return total


if __name__ == "__main__":
    with open("./inputs/day03/input.txt") as f:
        lines = f.readlines()
    reports = parse_inputs(lines)
    res_part_1 = solve_part_1(reports)
    print(f"{res_part_1=}")
    res_part_2 = solve_part_2(reports)
    print(f"{res_part_2=}")
