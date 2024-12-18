from collections.abc import Iterable, Sequence


def parse_inputs(lines: Iterable[str]) -> list[list[int]]:
    reports = []
    for line in lines:
        report = [int(level) for level in line.rstrip("\n").split(" ")]
        reports.append(report)
    return reports


def check_report(report: Sequence[int]) -> bool:
    n = len(report) - 1
    steps = [report[i + 1] - report[i] for i in range(n)]
    steps_abs = [abs(step) for step in steps]
    increasing = all(steps[i] > 0 for i in range(n))
    decreasing = all(steps[i] < 0 for i in range(n))
    in_range = all((steps_abs[i] >= 1) and (steps_abs[i] <= 3) for i in range(n))
    return (increasing or decreasing) and in_range


def solve_part_1(reports: Sequence[Sequence[int]]) -> int:
    count = 0
    for report in reports:
        count += check_report(report)

    return count


def solve_part_2(reports: Sequence[Sequence[int]]) -> int:
    count = 0
    for report in reports:
        res = check_report(report)
        if res:
            count += 1
            continue
        n = len(report)
        for i_removed in range(n):
            report_temp = [elem for i, elem in enumerate(report) if i != i_removed]
            res = check_report(report_temp)
            if res:
                count += 1
                break

    return count


if __name__ == "__main__":
    with open("./inputs/day02/input.txt") as f:
        lines = f.readlines()
    reports = parse_inputs(lines)
    res_part_1 = solve_part_1(reports)
    print(f"{res_part_1=}")
    res_part_2 = solve_part_2(reports)
    print(f"{res_part_2=}")
