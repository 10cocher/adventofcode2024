from collections import defaultdict
from collections.abc import Sequence


def one_update(a: int) -> int:
    divider = 16777216
    # First step
    b = 64 * a ^ a
    c = b % divider
    #
    # Second step
    d = c // 32 ^ c
    e = d % divider
    #
    # Third step
    f = 2048 * e ^ e
    g = f % divider
    return g


def solve_part_1(secrets: Sequence[int], n: int) -> int:
    total = 0
    for number in secrets:
        for i in range(n):
            number = one_update(number)
        total += number
    return total


def get_sequence_to_bananas(number: int, n: int) -> dict[str, int]:
    """Get the mapping 'sequence of diffs' -> 'number of bananas' for a single secret"""
    seq_to_value: dict[str, int] = {}
    #
    unit_digit = number % 10
    sequence = 4 * [-99]
    last_unit_digit = unit_digit
    #
    for i in range(n):
        number = one_update(number)
        unit_digit = number % 10
        diff = unit_digit - last_unit_digit
        #
        # Update the sequence of diffs
        for i in range(3):
            sequence[i] = sequence[i + 1]
        sequence[3] = diff
        #
        # Add the sequence to the dictionary if it's the first time we ecounter it
        seq_str = ",".join([str(j) for j in sequence])
        if seq_str not in seq_to_value:
            seq_to_value[seq_str] = unit_digit
        #
        last_unit_digit = unit_digit
    return seq_to_value


def solve_part_2(secrets: Sequence[int], n: int) -> int:
    # n_secrets = len(secrets)
    seq_to_bananas: dict[str, int] = defaultdict(int)
    for i_secret, secret in enumerate(secrets):
        seq_to_value: dict[str, int] = get_sequence_to_bananas(secret, n)
        for seq, value in seq_to_value.items():
            seq_to_bananas[seq] += value
        # print(f"After {i_secret+1:3}/{n_secrets:3}, {len(seq_to_bananas)} sequences")
    #
    max_bananas: int = max(seq_to_bananas.values())
    return max_bananas


if __name__ == "__main__":
    with open("./inputs/day22/input.txt") as f:
        lines = f.readlines()
    secrets: list[int] = [int(line.rstrip("\n")) for line in lines]

    res_part_1 = solve_part_1(secrets, n=2000)
    print(f"{res_part_1=}")
    res_part_2 = solve_part_2(secrets, n=2000)
    print(f"{res_part_2=}")
