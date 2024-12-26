from collections.abc import Sequence

TYPE_LOCK = list[int]


def parse_inputs(lines: Sequence[str]) -> tuple[list[str], list[str]]:
    new_block = True
    is_lock = True
    i_row = 0
    counts = [0, 0, 0, 0, 0]
    #
    locks: list[str] = []
    keys: list[str] = []
    #
    for line in lines:
        line = line.rstrip("\n")
        if line == "":
            if is_lock:
                locks.append(",".join([str(i) for i in counts]))
            else:
                keys.append(",".join([str(i) for i in counts]))
            new_block = True
            i_row = 0
            counts = [0, 0, 0, 0, 0]
            continue
        i_row += 1
        if new_block:
            is_lock = line == "#####"
            new_block = False
        if i_row in [1, 7]:
            continue
        for i_col, char in enumerate(line):
            if char == "#":
                counts[i_col] += 1

    if is_lock:
        locks.append(",".join([str(i) for i in counts]))
    else:
        keys.append(",".join([str(i) for i in counts]))

    print(f"{len(locks)} locks:")
    for lock in locks:
        print(lock)
    print(f"{len(locks)} keys:")
    for key in keys:
        print(key)

    return locks, keys


def check_pair(lock: str, key: str) -> bool:
    lock_int = [int(i) for i in lock.split(",")]
    key_int = [int(i) for i in key.split(",")]

    ok = True
    for a, b in zip(lock_int, key_int):
        if a + b > 5:
            ok = False
            break
    return ok


def solve_part_1(locks: list[str], keys: list[str]) -> int:
    total = 0
    for lock in locks:
        for key in keys:
            total += check_pair(lock, key)
    return total


def solve_part_2(locks: list[str], keys: list[str]) -> int:
    return 0


if __name__ == "__main__":
    with open("./inputs/day25/input.txt") as f:
        lines = f.readlines()
    locks, keys = parse_inputs(lines)
    #
    res_part_1 = solve_part_1(locks, keys)
    print(f"{res_part_1=}")
    res_part_2 = solve_part_2(locks, keys)
    print(f"{res_part_2=}")
