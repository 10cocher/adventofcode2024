import math
from collections import defaultdict
from collections.abc import Sequence


def next_power_of_2(x: int) -> int:
    return 1 if x == 0 else 2 ** math.ceil(math.log2(x))


def parse_inputs(lines: Sequence[str]) -> tuple[dict[str, int], list[int]]:
    for line in lines:
        line = line.rstrip("\n")
        if line.startswith("Register A"):
            a = int(line.lstrip("Register A:"))
        elif line.startswith("Register B"):
            b = int(line.lstrip("Register B:"))
        elif line.startswith("Register C"):
            c = int(line.lstrip("Register C:"))
        elif line.startswith("Program"):
            numbers = [int(i) for i in line.lstrip("Program :").split(",")]

    register = {"A": a, "B": b, "C": c}
    print(register)
    print(numbers)
    return register, numbers


def get_combo_operand(value: int, register: dict[str, int]) -> int:
    if value in [0, 1, 2, 3]:
        return value
    elif value == 4:
        return register["A"]
    elif value == 5:
        return register["B"]
    elif value == 6:
        return register["C"]
    else:
        raise ValueError(f"Impossible combo operand {value}")


def run_program(register_input: dict[str, int], numbers: list[int]) -> str:
    register: dict[str, int] = dict(register_input)
    #
    pointer: int = 0
    ok = True
    output: list[int] = []
    #
    opcode_to_register = {0: "A", 6: "B", 7: "C"}
    #
    while ok:
        opcode: int = numbers[pointer]
        operand: int = numbers[pointer + 1]
        #
        if opcode in [0, 6, 7]:  # adv, bdv, cdv
            numerator = register["A"]
            denominator = 2 ** get_combo_operand(operand, register)
            target_register = opcode_to_register[opcode]
            register[target_register] = int(numerator / denominator)
        elif opcode == 1:  # bxl
            register["B"] = register["B"] ^ operand
        elif opcode == 2:  # bst
            register["B"] = get_combo_operand(operand, register) % 8
        elif opcode == 3:  # jnz
            pass
        elif opcode == 4:  # bxc
            register["B"] = register["B"] ^ register["C"]
        elif opcode == 5:  # out
            output.append(get_combo_operand(operand, register) % 8)
            print(output)

        if (opcode == 3) and (register["A"] != 0):
            pointer = operand
        else:
            pointer += 2

        ok = 0 <= pointer < len(numbers)

    return ",".join([str(i) for i in output])


def run_program_and_check_sequence(
    register_input: dict[str, int], numbers: list[int]
) -> int:
    register: dict[str, int] = dict(register_input)
    #
    pointer: int = 0
    ok = True
    output: list[int] = []
    #
    opcode_to_register = {0: "A", 6: "B", 7: "C"}
    #
    while ok:
        opcode: int = numbers[pointer]
        operand: int = numbers[pointer + 1]
        #
        if opcode in [0, 6, 7]:  # adv, bdv, cdv
            numerator = register["A"]
            denominator = 2 ** get_combo_operand(operand, register)
            target_register = opcode_to_register[opcode]
            register[target_register] = int(numerator / denominator)
        elif opcode == 1:  # bxl
            register["B"] = register["B"] ^ operand
        elif opcode == 2:  # bst
            register["B"] = get_combo_operand(operand, register) % 8
        elif opcode == 3:  # jnz
            pass
        elif opcode == 4:  # bxc
            register["B"] = register["B"] ^ register["C"]
        elif opcode == 5:  # out
            output.append(get_combo_operand(operand, register) % 8)
            size = len(output)
            if size > len(numbers):
                return -99
            else:
                if output != numbers[:size]:
                    return size

        if (opcode == 3) and (register["A"] != 0):
            pointer = operand
        else:
            pointer += 2

        ok = 0 <= pointer < len(numbers)

    return len(output)


def get_processed_matches(matches: list[int]) -> list[int]:
    processed_matches = []
    processed_matches.append(matches[0])
    for i in range(1, len(matches)):
        if (matches[i] - matches[i - 1]) > 1:
            processed_matches.append(matches[i])
    return processed_matches


def solve_part_2(register_input: dict[str, int], numbers: list[int]) -> int:
    sizes: dict[int, list[int]] = defaultdict(list)
    test_register_A = 0
    best_size = 0
    success = False
    count = 0
    while not success:
        count += 1
        register_modified = dict(register_input)
        register_modified["A"] = test_register_A  # test_register_A
        size = run_program_and_check_sequence(register_modified, numbers)
        #
        # if size >= best_size:
        #    print(f"{best_size=} {test_register_A=} {size=}")
        #
        #
        if size == len(numbers):
            success = True
            print(f"SUCCESSS after {count} runs")
            return test_register_A
        elif best_size <= size < len(numbers):
            sizes[size].append(test_register_A)
            sizes[size - 1].append(test_register_A)
        #
        if size >= best_size:
            processed_matches = get_processed_matches(sizes[size])
            if len(processed_matches) < 3:
                print(f"{size=} {best_size=}", get_processed_matches(sizes[size]))
        if size > best_size:
            print(f">>>>>>> Match of length {size} found: {test_register_A=}")
            best_size = size
        #
        # Determine the new number to test
        if best_size < 2:
            # No need to do something fancy for now. Let us spare the reflection about
            # the dreaded "1" case
            candidate_test_register_A = test_register_A + 1
        # elif size == best_size:
        #    # Looks like we are on a good track
        #    candidate_test_register_A = test_register_A + 1
        else:
            matches = sizes[best_size]
            # print(f"{matches=}")
            # if len(matches) == 1:
            #    multiple = test_register_A // matches[0]
            #    test_register_A = (multiple + 1) * matches[0]
            # elif len(matches) >= 2:
            processed_matches = get_processed_matches(matches)
            next_power = next_power_of_2(matches[0])
            # candidate_test_register_A = processed_matches[-1] + next_power
            reference = processed_matches[0]
            multiple = (test_register_A - reference) // next_power
            # print(f"{next_power=} {candidate_test_register_A=}")
            candidate_test_register_A = reference + next_power * (multiple + 1)
            # if len(processed_matches) == 1:
            #    # Try a new multiple
            #    n_multiples = test_register_A // processed_matches[0]
            #    candidate_test_register_A = (n_multiples+1) * processed_matches[0]
            # else:
            #    reference = processed_matches[0]
            #    delta = processed_matches[1] - reference
            #    # print(f"{best_size=} {matches=} {delta=}")
            #    multiple = (test_register_A - reference) // delta
            #    candidate_test_register_A = reference + delta * (multiple + 1)

        # Ensure we are not skipping a power of 2, this could be interesting
        # next_power = next_power_of_2(test_register_A)
        # if next_power == 4096:
        #    print("hello", next_power, test_register_A, candidate_test_register_A)
        # if next_power == test_register_A:
        #    # We juste tested a power of 2
        #    test_register_A = candidate_test_register_A
        # else:
        #    test_register_A = min(next_power, candidate_test_register_A)
        if test_register_A == candidate_test_register_A:
            success = True

        test_register_A = candidate_test_register_A

        if test_register_A > 10**7:  # 117445:
            success = True
        # test_register_A += 1

    print(f"FAILURE after {count} runs.")
    print(f"I was looking for a sequence of size {len(numbers)}. Found {best_size=}")

    return -1


# 4096
# 32768
if __name__ == "__main__":
    with open("./inputs/day17/input.txt") as f:
        lines = f.readlines()
    register, numbers = parse_inputs(lines)
    res_part_1 = run_program(register, numbers)
    print(f"{res_part_1=}")
    # for i in range(8):
    #    print(i, next_power_of_2(i+1))
    res_part_2 = solve_part_2(register, numbers)
    print(f"{res_part_2=}")
