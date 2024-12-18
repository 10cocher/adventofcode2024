from collections.abc import Sequence


def parse_inputs(lines: Sequence[str]) -> tuple[dict[int, int], list[int]]:
    id_to_count: dict[int, int] = {}
    free: list[int] = []
    #
    name = 0
    line = lines[0].rstrip("\n")
    for i, c in enumerate(line):
        if i % 2 == 0:
            id_to_count[name] = int(c)
            name += 1
        else:
            free.append(int(c))
    return id_to_count, free


def parse_inputs_for_part2(lines: Sequence[str]) -> list[tuple[int, int]]:
    blocks: list[tuple[int, int]] = []
    #
    name = 0
    line = lines[0].rstrip("\n")
    #
    for i, c in enumerate(line):
        if i % 2 == 0:
            blocks.append((name, int(c)))
        else:
            if int(c) > 0:
                blocks.append((-1, int(c)))
            name += 1
    return blocks


def solve_part_1(id_to_count: dict[int, int], free: list[int]) -> int:
    total = 0
    pos = 0
    max_id = max(id_to_count.keys())
    names = list(id_to_count.keys())
    #
    for name in names:
        count = id_to_count[name]
        if count < 1:
            print("what?")
            break
            continue
        coeffs = range(pos, pos + count)
        total += name * sum(coeffs)
        pos += count
        id_to_count[name] = 0
        if id_to_count[name + 1] < 1:
            break
        #
        for i in range(free[name]):
            total += max_id * pos
            id_to_count[max_id] += -1
            pos += 1
            while (max_id >= name) and id_to_count[max_id] == 0:
                max_id += -1

            if max_id <= name:
                break

    # 6520497170536 too high
    # 6519155389266
    return total


def solve_part_2(blocks: list[tuple[int, int]]) -> int:
    last_block = max(block[0] for block in blocks)
    for b_to_move in range(last_block, 0, -1):
        print(f">>>>> {b_to_move}")
        # Find the index of the block. This is awful code. I'm ashamed
        n = len(blocks)
        index_to_move = n - 1
        while blocks[index_to_move][0] != b_to_move:
            index_to_move -= 1
        size_to_move = blocks[index_to_move][1]
        #
        for index_candidate in range(1, index_to_move):
            candidate_name, candidate_size = blocks[index_candidate]
            if candidate_name != -1:
                continue
            if size_to_move > candidate_size:
                continue
            elif size_to_move == candidate_size:
                blocks[index_candidate] = (b_to_move, size_to_move)
                blocks[index_to_move] = (-1, size_to_move)
                # print(f"moved exactly to {index_candidate}")
                break
            else:
                blocks[index_candidate] = (b_to_move, size_to_move)
                blocks[index_to_move] = (-1, size_to_move)
                blocks.insert(index_candidate + 1, (-1, candidate_size - size_to_move))
                # print(f"moved in larger position {index_candidate}")
                break

    print("Finished sorting the thing")
    pos = 0
    total = 0
    for block_id, size in blocks:
        if block_id != -1:
            total += block_id * sum(range(pos, pos + size))
        pos += size
    return total


if __name__ == "__main__":
    with open("./inputs/day09/input.txt") as f:
        lines = f.readlines()
    id_to_count, free = parse_inputs(lines)
    res_part_1 = solve_part_1(id_to_count, free)
    blocks = parse_inputs_for_part2(lines)
    print(f"{res_part_1=}")
    res_part_2 = solve_part_2(blocks)
    print(f"{res_part_2=}")
