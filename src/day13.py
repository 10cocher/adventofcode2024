from collections.abc import Sequence

TYPE_EQ = dict[str, int]


def parse_inputs(lines: Sequence[str]) -> list[TYPE_EQ]:
    #
    patternA = "Button A: X+"
    patternB = "Button B: X+"
    patternY = ", Y+"
    patternPX = "Prize: X="
    patternPY = ", Y="
    #
    eqs: list[TYPE_EQ] = []
    coeffs: TYPE_EQ = {}
    for line in lines:
        line = line.rstrip("\n")
        if line == "":
            eqs.append(coeffs)
            print(coeffs)
            coeffs = {}
        elif line.startswith(patternA):
            ax, ay = line.replace(patternA, "").replace(patternY, ",").split(",")
            coeffs.update({"ax": int(ax), "ay": int(ay)})
        elif line.startswith(patternB):
            bx, by = line.replace(patternB, "").replace(patternY, ",").split(",")
            coeffs.update({"bx": int(bx), "by": int(by)})
        elif line.startswith(patternPX):
            px, py = line.replace(patternPX, "").replace(patternPY, ",").split(",")
            coeffs.update({"px": int(px), "py": int(py)})
    eqs.append(coeffs)
    return eqs


def solve_one_system(coeffs: TYPE_EQ) -> tuple[int, int]:
    """
    ax * A + bx * B = px
    ay * A + bY * B = pY
    ----------------------
    by*ax*A + by*bx*B = by*px
    bx*ay*A + bx*bY*B = bx*pY
    --------
    (by*ax - bx*ay)A = (by*px - bx*py)
    A = (by*px - bx*py) / (by*ax - bx*ay)
    ------
    ay*ax*A + ay*bx*A = ay*px
    ax*ay*A + ax*by*B = ax*py
    B =  (ay*px * ax*px) / (ay*bx + ax*by)
    """
    ax = coeffs["ax"]
    ay = coeffs["ay"]
    bx = coeffs["bx"]
    by = coeffs["by"]
    px = coeffs["px"] + 10000000000000
    py = coeffs["py"] + 10000000000000
    #
    numA = by * px - bx * py
    denA = by * ax - bx * ay
    #
    numB = ay * px - ax * py
    denB = ay * bx - ax * by
    #
    if (numA % denA == 0) and (numB % denB == 0):
        A = numA // denA
        B = numB // denB
    else:
        A = -1
        B = -1
    print(f"{A=} {B=}")
    return A, B


def solve_part_1(eqs: list[TYPE_EQ]) -> int:
    total = 0
    for eq in eqs:
        a, b = solve_one_system(eq)
        # tokens = (3 * a + b) if ((0 <= a <= 100) and (0 <= b <= 100)) else 0
        tokens = (3 * a + b) if ((a >= 0) and (b >= 0)) else 0
        total += tokens

    # 82570698599774 too low
    return total


def solve_part_2(eqs: list[TYPE_EQ]) -> int:
    return 0


if __name__ == "__main__":
    with open("./inputs/day13/input.txt") as f:
        lines = f.readlines()
    eqs = parse_inputs(lines)
    res_part_1 = solve_part_1(eqs)
    print(f"{res_part_1=}")
    res_part_2 = solve_part_2(eqs)
    print(f"{res_part_2=}")
