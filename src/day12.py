from collections import defaultdict
from collections.abc import Iterable, Sequence

TYPE_HEATMAP = dict[complex, str]
TYPE_POLYGON = dict[complex, dict[str, bool]]
TYPE_POLYGONS = dict[str, TYPE_POLYGON]


def parse_inputs(lines: Sequence[str]) -> tuple[TYPE_HEATMAP, int, int]:
    n_rows = len(lines)
    n_cols = len(lines[0].rstrip("\n"))
    heatmap: TYPE_HEATMAP = {}
    #
    for i_row, line in enumerate(lines):
        line = line.rstrip("\n")
        for i_col, char in enumerate(line):
            heatmap[complex(i_col, i_row)] = char
    return heatmap, n_rows, n_cols


diffs = {
    "right": complex(1, 0),
    "top": complex(0, 1),
    "left": complex(-1, 0),
    "bottom": complex(0, -1),
}


def delineate(heatmap: TYPE_HEATMAP, n_rows: int, n_cols: int) -> TYPE_POLYGONS:
    """Identify all polygons and get the list of (x,y) coordinates that belong to each
    of them"""
    # side_to_border: False if the polygon "extends" toward that direction (left, right,
    # bottom, top), True otherwise
    side_to_border: dict[str, bool]
    new_polygon: TYPE_POLYGON
    include_in: set[str]
    char_to_polygons_count: dict[str, int] = defaultdict(int)
    #
    count = 0
    polygons: TYPE_POLYGONS = {}
    for i_row in range(n_rows):
        for i_col in range(n_cols):
            count += 1
            pos = complex(i_col, i_row)
            char = heatmap[pos]
            #
            include_in = set()
            side_to_border = {}
            # Check all neighbours one by one
            for side, increment in diffs.items():
                neighbour_pos = pos + increment
                try:
                    neighbour_char = heatmap[neighbour_pos]
                except KeyError:
                    border = True
                else:
                    border = neighbour_char != char
                    if (not border) and (side in ["left", "bottom"]):
                        # Try to assign an existing polygon to this char
                        for candidate_polygon_name, polygon in polygons.items():
                            if candidate_polygon_name[0] != char:
                                continue
                            if neighbour_pos in polygon:
                                include_in.add(candidate_polygon_name)
                side_to_border[side] = border
            if len(include_in) == 0:
                char_to_polygons_count[char] += 1
                index = char_to_polygons_count[char]
                polygon_name = char + str(index)
                new_polygon = {pos: side_to_border}
                polygons[polygon_name] = new_polygon
            elif len(include_in) == 1:
                polygon_name = list(include_in)[0]
                polygons[polygon_name][pos] = side_to_border
            elif len(include_in) == 2:
                p0, p1 = sorted(include_in)
                polygons[p0].update(polygons[p1])
                del polygons[p1]
                polygons[p0][pos] = side_to_border
    return polygons


def solve_part_1(polygons: TYPE_POLYGONS) -> int:
    total = 0
    for polygon_name, polygon in polygons.items():
        area = len(polygon)
        perimeter = sum(
            [sum(side_to_border.values()) for _, side_to_border in polygon.items()]
        )
        # print(f"{polygon_name=} {area=:2} {perimeter=:2}")
        total += area * perimeter
    return total


def process_one_polygon(elements: Iterable[complex]) -> int:
    """Compute custom permiter for part 2"""
    # Restrict x and y to where the polygon lies, to not loop over useless coordinates
    unique_x: set[int] = {int(pos.real) for pos in elements}
    unique_y: set[int] = {int(pos.imag) for pos in elements}
    minx = min(unique_x)
    maxx = max(unique_x)
    miny = min(unique_y)
    maxy = max(unique_y)
    #
    total = 0

    # Handle vertical borders by checking where borders are columns after columns
    # Convention:
    # - "4L" left-border between positions (3, y0) and (4, y0)
    # - "4R": right-border between bositions (3, y0) and (4, y0)
    borders_prev: set[str] = set()
    borders: set[str]
    x_index: list[int]
    for y in range(miny, maxy + 1):
        x_index = sorted({int(pos.real) for pos in elements if int(pos.imag) == y})
        borders = {f"{x_index[0]}L", f"{x_index[-1] + 1}R"}
        holes_index = [
            i for i in range(len(x_index) - 1) if (x_index[i + 1] - x_index[i] > 1)
        ]
        for i_hole in holes_index:
            borders.add(f"{x_index[i_hole] + 1}R")
            borders.add(f"{x_index[i_hole + 1]}L")
        created = borders - borders_prev
        total += len(created)
        borders_prev = borders
    #
    # Do the same for the horizontal borders
    borders_prev = set()
    y_index: list[int]
    for x in range(minx, maxx + 1):
        y_index = sorted({int(pos.imag) for pos in elements if int(pos.real) == x})
        borders = {f"{y_index[0]}B", f"{y_index[-1] + 1}T"}
        holes_index = [
            i for i in range(len(y_index) - 1) if (y_index[i + 1] - y_index[i] > 1)
        ]
        for i_hole in holes_index:
            borders.add(f"{y_index[i_hole] + 1}T")
            borders.add(f"{y_index[i_hole + 1]}B")
        created = borders - borders_prev
        total += len(created)
        borders_prev = borders
    return total


def solve_part_2(polygons: TYPE_POLYGONS) -> int:
    total = 0
    for polygon_name, polygon in polygons.items():
        area = len(polygon)
        custom_perimeter = process_one_polygon(polygon.keys())
        # print(f"{polygon_name=} {area=:2} {custom_perimeter=:2}")
        total += area * custom_perimeter
    return total


if __name__ == "__main__":
    with open("./inputs/day12/input.txt") as f:
        lines = f.readlines()
    heatmap, n_rows, n_cols = parse_inputs(lines)
    polygons = delineate(heatmap, n_rows, n_cols)
    res_part_1 = solve_part_1(polygons)
    print(f"{res_part_1=}")
    res_part_2 = solve_part_2(polygons)
    print(f"{res_part_2=}")
