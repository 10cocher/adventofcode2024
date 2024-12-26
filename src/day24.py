from collections.abc import Sequence

TYPE_WIRES = dict[str, bool | None]
TYPE_CONNECTIONS = dict[str, tuple[str, str, str]]


def parse_inputs(lines: Sequence[str]) -> tuple[TYPE_WIRES, TYPE_CONNECTIONS]:
    wires: TYPE_WIRES = {}
    connections: TYPE_CONNECTIONS = {}
    #
    finished_wires = False
    for line in lines:
        line = line.rstrip("\n")
        if not line:
            finished_wires = True
            continue
        #
        if finished_wires:
            operation, destination_wire = line.split("->")
            operation = operation.strip()
            destination_wire = destination_wire.strip()
            left_wire, operator, right_wire = operation.split(" ")
            #
            wires[destination_wire] = None
            connections[destination_wire] = (operator, left_wire, right_wire)
        else:
            wire_name, wire_value = line.split(":")
            wires[wire_name] = bool(int(wire_value.strip()))
    return wires, connections


def solve_part_1(wires: TYPE_WIRES, connections: TYPE_CONNECTIONS) -> tuple[str, int]:
    while any(wire_value is None for _, wire_value in wires.items()):
        for wire_name, wire_value in wires.items():
            if wire_value is not None:
                continue
            operator, left_name, right_name = connections[wire_name]
            left = wires[left_name]
            right = wires[right_name]
            if (left is not None) and (right is not None):
                if operator == "AND":
                    wires[wire_name] = left and right
                elif operator == "OR":
                    wires[wire_name] = left or right
                elif operator == "XOR":
                    wires[wire_name] = left ^ right
                else:
                    raise ValueError(f"Unknown {operator=}")
    #
    bin_result: str = ""
    z_wires = sorted(
        [wire_name for wire_name in wires if wire_name.startswith("z")], reverse=True
    )
    for wire_name in z_wires:
        wire_value = wires[wire_name]
        if wire_value is None:
            raise ValueError()
        bin_result += str(int(wire_value))
    # print(bin_result)
    return bin_result, int(bin_result, 2)


# ################
# Utils for part 2
# ################


def get_wires_count(
    wires: TYPE_WIRES,
) -> tuple[list[str], list[str], list[str], list[str]]:
    """Group wires by x,y,z or other wires."""
    x_wires: list[str] = []
    y_wires: list[str] = []
    z_wires: list[str] = []
    other_wires: list[str] = []
    for wire in sorted(wires):
        if wire.startswith("x"):
            x_wires.append(wire)
        elif wire.startswith("y"):
            y_wires.append(wire)
        elif wire.startswith("z"):
            z_wires.append(wire)
        else:
            other_wires.append(wire)
    return x_wires, y_wires, z_wires, other_wires


def compute_result(
    n1: int,
    n2: int,
    wires: TYPE_WIRES,
    connections: TYPE_CONNECTIONS,
) -> tuple[int, int, list[int]]:
    """Compute the actual addition of 2**n and 2**m to find suspicious digits."""
    # Reset everything
    for wire_name in wires:
        if wire_name.startswith(("x", "y")):
            wires[wire_name] = False
        else:
            wires[wire_name] = None
    #
    # Compute binary representation of inputs
    bin1 = f"{n1:b}"
    bin2 = f"{n2:b}"
    #
    # Compute expected result
    result = n1 + n2
    bin_result = f"{result:b}"
    #
    # Compute actual result
    for i, char in enumerate(bin1[::-1]):
        wires[f"x{i:02}"] = bool(int(char))
    for i, char in enumerate(bin2[::-1]):
        wires[f"y{i:02}"] = bool(int(char))
    #
    bin_actual, actual = solve_part_1(wires, connections)
    #
    if result != actual:
        reverse_bin_result = bin_result[::-1]
        reverse_bin_actual = bin_actual[::-1]
        differing_bits = [
            i
            for i, char in enumerate(reverse_bin_result)
            if char != reverse_bin_actual[i]
        ]
    else:
        differing_bits = []

    return result, actual, differing_bits


def explore(wires: TYPE_WIRES, connections: TYPE_CONNECTIONS) -> None:
    """Print how many wires we have + the output wires that seems to be wrong."""
    x_wires, y_wires, z_wires, other_wires = get_wires_count(wires)
    print(f"{len(x_wires)} x-wires")
    print(f"{len(y_wires)} y-wires")
    print(f"{len(z_wires)} z-wires")
    print(f"{len(other_wires)}  other wires")
    #
    n = len(x_wires)

    suspect_bits: set[int] = set()
    # ok = False
    for i in range(n):
        for j in range(n):
            n1 = 2**i
            n2 = 2**j
            result, actual, differing_bits = compute_result(n1, n2, wires, connections)
            for bit in differing_bits:
                suspect_bits.add(bit)
            # if result != actual:
            #    print(f"{i=}, {j=}, {n1=}, {n2=}, {result=}, {actual=}")
            #    ok = True
            #    break
    n_suspect_bits = len(suspect_bits)
    print(f"{n_suspect_bits}/{len(z_wires)} suspect_bits", sorted(suspect_bits))
    #
    return


def find_instruction(
    operator: str, left: str, right: str, connections: TYPE_CONNECTIONS
) -> str:
    """Check if an instruction exists in the listing and return the name of the wire
    containing the result."""
    for output, equation in connections.items():
        if (equation == (operator, left, right)) or (
            equation == (operator, right, left)
        ):
            return output
    raise ValueError(f"Did not find '{left} {operator} {right}'")


def get_written_instruction(output: str, connections: TYPE_CONNECTIONS) -> str:
    """Pretty-print an instruction."""
    op, a, b = connections[output]
    return f"{output} = {a} {op} {b}"


def get_all_operations_for_one_output(
    z_index: int, connections: TYPE_CONNECTIONS
) -> set[str]:
    """List all the operations that lead to an output digit."""
    to_unpack: set[str] = {f"z{z_index:02}"}
    #
    n_operations = 0
    operations: set[str] = set()
    while len(to_unpack) > 0:
        new_to_unpack = set()
        for wire in to_unpack:
            _, left, right = connections[wire]
            operation = get_written_instruction(wire, connections)
            # print(operation)
            operations.add(operation)
            n_operations += 1
            if not left.startswith(("x", "y")):
                new_to_unpack.add(left)
            if not right.startswith(("x", "y")):
                new_to_unpack.add(right)
        to_unpack = new_to_unpack

    # print(f"{z_index=} {n_operations}")
    return operations


def guess_next_instructions(
    i: int, connections: TYPE_CONNECTIONS, verbose: bool = False
) -> set[str]:
    x = f"x{i:02}"
    y = f"y{i:02}"
    z = f"z{i:02}"
    prev_x = f"x{(i-1):02}"
    prev_y = f"y{(i-1):02}"
    prev_z = f"z{(i-1):02}"
    #
    instructions: set[str] = set()
    #
    # Instruction 2
    output_and2 = find_instruction("AND", prev_x, prev_y, connections)
    instruction = get_written_instruction(output_and2, connections)
    if verbose:
        print(f"===> {instruction}")
    instructions.add(instruction)
    #
    # Instruction 4
    output_xor1 = find_instruction("XOR", x, y, connections)
    instruction = get_written_instruction(output_xor1, connections)
    if verbose:
        print(f"===> {instruction}")
    instructions.add(instruction)
    #
    # Instruction 1
    previous_output = connections[prev_z]  # should be a XOR between
    op, a, b = previous_output
    if op != "XOR":
        raise ValueError(f"Expected XOR instead of {op} between {a} and {b}")
    #
    output_and1 = find_instruction("AND", a, b, connections)
    instruction = get_written_instruction(output_and1, connections)
    if verbose:
        print(f"===> {instruction}")
    instructions.add(instruction)
    #
    # Instruction 3
    output_or = find_instruction("OR", output_and1, output_and2, connections)
    instruction = get_written_instruction(output_or, connections)
    if verbose:
        print(f"===> {instruction}")
    instructions.add(instruction)
    #
    # Instruction 5
    output_xor2 = find_instruction("XOR", output_xor1, output_or, connections)
    instruction = get_written_instruction(output_xor2, connections)
    if verbose:
        print(f"===> {instruction}")
    instructions.add(instruction)
    if output_xor2 != z:
        print(f"/!\ {output_xor2} should be swapped with {z}")

    return instructions


def swap_wires(
    connections: TYPE_CONNECTIONS, wire_a: str, wire_b: str
) -> TYPE_CONNECTIONS:
    new_connections: TYPE_CONNECTIONS = {}
    for output, (operator, x, y) in connections.items():
        new_output: str
        if output == wire_a:
            new_output = wire_b
        elif output == wire_b:
            new_output = wire_a
        else:
            new_output = output
        new_connections[new_output] = (operator, x, y)
    return new_connections


# ############
# Solve part 2
# ############


def solve_part_2(
    wires_to_be_swapped: set[tuple[str, str]], connections: TYPE_CONNECTIONS
) -> str:
    # output digits that seem incorrect
    verbose_digits = [10, 11, 21, 22, 33, 34, 39, 40]
    #
    set_swapped_wires: set[str] = set()
    for wire_a, wire_b in wires_to_be_swapped:
        connections = swap_wires(connections, wire_a, wire_b)
        set_swapped_wires.add(wire_a)
        set_swapped_wires.add(wire_b)
    #
    z_wires = {wire for wire in connections if wire.startswith("z")}
    last_digit = int(sorted(z_wires)[-1].lstrip("z"))
    #
    digit_to_operations: dict[int, set[str]] = {}
    for i in range(last_digit + 1):
        verbose = i in verbose_digits
        print(f"=== {i=} ===")
        operations = get_all_operations_for_one_output(i, connections)
        digit_to_operations[i] = operations
        if (i >= 2) and (i < last_digit):
            new_operations = operations - digit_to_operations[i - 1]
            n_new = len(new_operations)
            if verbose:
                print(f"{n_new} operations")
            if verbose:
                for operation in new_operations:
                    print(operation)
            try:
                expected_new_operations = guess_next_instructions(
                    i, connections, verbose=verbose
                )
            except ValueError as e:
                print("WARNING", e)

            n_expected = len(expected_new_operations)
            ok = new_operations == expected_new_operations
            if verbose:
                if ok:
                    print(f"OK: expected {n_expected}, found {n_new} identical")
                else:
                    print(f"Oh!: expected {n_expected}, found {n_new}")
    explore(wires, connections)
    return ",".join(sorted(set_swapped_wires))


if __name__ == "__main__":
    with open("./inputs/day24/input.txt") as f:
        lines = f.readlines()
    wires, connections = parse_inputs(lines)
    #
    _, res_part_1 = solve_part_1(wires, connections)
    print(f"{res_part_1=}")
    #
    # Manually add the pair of wires to be swapped as far as you find them.
    # Start with an empty list and run the script at first. This should give some
    # clue on which pairs should be added.
    wires_to_be_swapped: set[tuple[str, str]] = {
        ("gpr", "z10"),
        ("ghp", "z33"),
        ("nks", "z21"),
        ("cpm", "krs"),
    }
    #
    res_part_2 = solve_part_2(wires_to_be_swapped, connections)
    print(f"{res_part_2=}")
