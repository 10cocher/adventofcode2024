import itertools
from collections import defaultdict

numeric_keypad: dict[str, complex] = {
    "X": complex(0, 0),
    "0": complex(1, 0),
    "A": complex(2, 0),
    "1": complex(0, 1),
    "2": complex(1, 1),
    "3": complex(2, 1),
    "4": complex(0, 2),
    "5": complex(1, 2),
    "6": complex(2, 2),
    "7": complex(0, 3),
    "8": complex(1, 3),
    "9": complex(2, 3),
}

directional_keypad: dict[str, complex] = {
    "<": complex(0, 0),
    "v": complex(1, 0),
    ">": complex(2, 0),
    "X": complex(0, 1),
    "^": complex(1, 1),
    "A": complex(2, 1),
}

BUTTON_TO_MOVE: dict[str, complex] = {
    ">": complex(1, 0),
    "^": complex(0, 1),
    "<": complex(-1, 0),
    "v": complex(0, -1),
}

# EXEMPLES = {
#    "379A": [
#        "^A<<^^A>>AvvvA",
#        "<A>Av<<AA>^AA>AvAA^A<vAAA>^A",
#        "<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A#",
#    ]
# }


def reverse(sequence: str, keypad: dict[str, complex]) -> str:
    reverse_keypad = {v: k for k, v in keypad.items()}
    position = "A"
    coord = keypad[position]
    output = ""
    for char in sequence:
        if char == "A":
            output += position
        else:
            coord += BUTTON_TO_MOVE[char]
            position = reverse_keypad[coord]
        print(f"{char=} {coord=} {position=} {output=}")
    return output


def validate_seq(
    sequence: str, start_coord: complex, keypad: dict[str, complex]
) -> bool:
    coords: set[complex] = set()
    coord = start_coord
    for move in sequence:
        coords.add(coord)
        coord = coord + BUTTON_TO_MOVE[move]
    return keypad["X"] not in coords


def get_keypad_sequence(
    code: str, keypad: dict[str, complex], explore_everything: bool = True
) -> list[str]:
    all_sequences: list[str] = [""]
    new_all_sequences: list[str]
    position = "A"
    coord = keypad[position]
    for new_position in code:
        new_coord = keypad[new_position]
        delta = new_coord - coord
        dy = int(delta.imag)
        dx = int(delta.real)
        #
        new_yseq = dy * "^" if (dy > 0) else (-dy) * "v"
        new_xseq = dx * ">" if (dx > 0) else (-dx) * "<"
        #
        if explore_everything:
            # Explore everything
            new_seq = new_yseq + new_xseq
            candidate_new_seqs: set[str] = {
                "".join(sequence)
                for sequence in set(itertools.permutations(new_seq, len(new_seq)))
            }
            new_seqs: set[str] = {
                seq + "A"
                for seq in candidate_new_seqs
                if validate_seq(seq, coord, keypad)
            }
        else:
            if keypad["X"] == complex(0, 0):
                # numeric keypad
                new_seq = new_yseq + new_xseq if (dy > 0) else new_xseq + new_yseq
            elif keypad["X"] == complex(0, 1):
                # directional keypad
                new_seq = new_xseq + new_yseq if (dy > 0) else new_yseq + new_xseq
            else:
                raise ValueError()
            new_seqs = {new_seq + "A"}

        #
        new_all_sequences = []
        for beginning in all_sequences:
            for new_seq in new_seqs:
                new_all_sequences.append(beginning + new_seq)
        #
        all_sequences = new_all_sequences
        position = new_position
        coord = new_coord

    return all_sequences


def parse_one_code(code: str) -> int:
    print("Step 1: numeric keypad")
    all_sequences_1: list[str] = get_keypad_sequence(code, numeric_keypad)
    print(f"Step 1: found {len(all_sequences_1)} sequences")
    # for seq1 in all_sequences_1:
    #     print(seq1)
    #
    print("Step 2: directional keypad")
    all_sequences_2: list[str] = []
    for seq1 in all_sequences_1:
        seqs2 = get_keypad_sequence(seq1, directional_keypad)
        all_sequences_2.extend(seqs2)
    print(f"Step 2: found {len(all_sequences_2)} sequences")
    # for seq2 in all_sequences_2:
    #     print(seq2)

    print("Step 3: directional keypad")
    all_sequences_3: list[str] = []
    for seq2 in all_sequences_2:
        seqs3 = get_keypad_sequence(seq2, directional_keypad)
        all_sequences_3.extend(seqs3)
    print(f"Step 3: found {len(all_sequences_3)} sequences")
    for seq3 in seqs3:
        print(f"RSLT {seq3}")
    #
    length_to_count: dict[int, int] = defaultdict(int)
    for seq3 in all_sequences_3:
        length = len(seq3)
        length_to_count[length] += 1
    # for k, v in length_to_count.items():
    #    print(f"RSLT {k=} {v=}")
    min_length = min(length_to_count.keys())
    numeric_code = int(code[:3])
    print(f"{min_length=} {numeric_code=}")
    #
    #
    code_to_e3 = {
        "029A": "<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A",
        "980A": "<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A",
        "179A": "<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A",
        "456A": "<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A",
        "379A": "<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A",
    }
    e3 = code_to_e3[code]
    print("E3XX", e3)
    # print("Test e3", e3 in all_sequences_3)
    # e3 = "<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A"
    # e2 = "v<<A>>^A<A>AvA<^AA>A<vAAA>^A"
    # e1 = "<A^A>^^AvvvA"
    # print(e1 in all_sequences_1)
    # print(e2 in all_sequences_2)
    # print(e3 in all_sequences_3)
    #
    return numeric_code * min_length


def get_sequences_stats(sequences: list[str], log: bool = False) -> dict[int, int]:
    length_to_count: dict[int, int] = defaultdict(int)
    for seq in sequences:
        length = len(seq)
        length_to_count[length] += 1
    if log:
        for length, count in sorted(length_to_count.items()):
            print(f"{count} sequences of length {length}")
    return length_to_count


def parse_one_code_bis(code: str, n_robots: int) -> int:
    all_sequences: list[str] = get_keypad_sequence(
        code, numeric_keypad, explore_everything=True
    )
    print(f"   Step 1: found {len(all_sequences)} sequences")
    for seq in sorted(all_sequences):
        print(len(seq), seq)
    length_to_count = get_sequences_stats(all_sequences, log=True)

    # CODE_TO_FIND = "^A<<^^A>>AvvvA"
    # CODE_TO_FIND ="<A>Av<<AA>^AA>AvAA^A<vAAA>^A"
    # CODE_TO_FIND = "<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A"

    for i_robot in range(n_robots):
        new_all_sequences: list[str] = []
        for seq in all_sequences:
            new_sequences = get_keypad_sequence(seq, directional_keypad)
            new_all_sequences.extend(new_sequences)
        print(f"{i_robot=}: found {len(new_all_sequences)} sequences")
        length_to_count = get_sequences_stats(new_all_sequences, log=False)
        min_length = min(length_to_count.keys())
        all_sequences = [s for s in new_all_sequences if len(s) == min_length]
        if i_robot < 1:
            for seq in sorted(all_sequences):
                print(len(seq), seq)
        # all_sequences = new_all_sequences
    #
    length_to_count = get_sequences_stats(all_sequences, log=False)
    min_length = min(length_to_count.keys())
    #
    numeric_code = int(code[:3])
    print(f"{min_length=} {numeric_code=}")
    #
    return numeric_code * min_length


if __name__ == "__main__":
    with open("./inputs/day21/input0.txt") as f:
        codes = [line.rstrip("\n") for line in f.readlines()]

    res_part_1 = 0
    for code in codes:
        # if code != "379A":
        #     continue
        print("=======================")
        print(f"=== {code=} =======")
        print("=======================")
        res_part_1 += parse_one_code_bis(code, n_robots=2)
        # break
    print("~~~~")
    print("~~~~")
    print("~~~~")
    print(f"{res_part_1=}")

    # print(f"{word=}")
    # new_word = reverse(word, keypad=directional_keypad)
    # print(f"{new_word=}")
    # decoded = reverse(new_word, keypad=numeric_keypad)
    # print(f"{decoded=}")
