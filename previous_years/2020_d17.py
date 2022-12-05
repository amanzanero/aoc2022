from pathlib import Path
from enum import Enum
from dataclasses import dataclass
from collections import defaultdict


class State(Enum):
    Active = '#'
    Inactive = '.'

    def __str__(self):
        return self.value


@dataclass()
class Cube:
    x: int
    y: int
    z: int

    def is_active(self, cubes):
        if self.x < 0 \
                or self.y < 0 \
                or self.z < 0 \
                or self.z >= len(cubes) \
                or self.x >= len(cubes[0]) \
                or self.y >= len(cubes[0][0]):
            return False
        else:
            state = cubes[self.z][self.x][self.y]
            return state == State.Active

    def __hash__(self):
        return hash((self.x, self.y, self.z))


@dataclass()
class HCube:
    x: int
    y: int
    z: int
    w: int

    def is_active(self, cubes):
        if self.x < 0 \
                or self.y < 0 \
                or self.z < 0 \
                or self.w < 0 \
                or self.w >= len(cubes) \
                or self.z >= len(cubes[0]) \
                or self.x >= len(cubes[0][0]) \
                or self.y >= len(cubes[0][0][0]):
            return False
        else:
            state = cubes[self.w][self.z][self.x][self.y]
            return state == State.Active

    def __hash__(self):
        return hash((self.x, self.y, self.z))


def parse_input(lines: str):
    l_split = lines.split()
    init_state = []
    for line in l_split:
        parsed_line = [State(state) for state in line]
        init_state.append(parsed_line)
    return init_state


def get_neighbors(cube: Cube):
    neighbors = []
    for i in (0, -1, 1):
        for j in (0, -1, 1):
            for k in (0, -1, 1):
                neighbor = Cube(
                    cube.x + i,
                    cube.y + j,
                    cube.z + k,
                )
                if neighbor == cube:
                    continue
                neighbors.append(neighbor)
    return neighbors


def next_state(cubes_to_make_active):
    max_x = max(cubes_to_make_active, key=lambda cube: cube.x).x
    min_x = min(cubes_to_make_active, key=lambda cube: cube.x).x
    max_y = max(cubes_to_make_active, key=lambda cube: cube.y).y
    min_y = min(cubes_to_make_active, key=lambda cube: cube.y).y
    max_z = max(cubes_to_make_active, key=lambda cube: cube.z).z
    min_z = min(cubes_to_make_active, key=lambda cube: cube.z).z

    len_x = max_x - min_x + 1
    len_y = max_y - min_y + 1
    len_z = max_z - min_z + 1

    cubes = [
        [
            [
                State.Inactive for _ in range(len_y)
            ] for _ in range(len_x)
        ] for _ in range(len_z)
    ]

    for cube in cubes_to_make_active:
        cubes[cube.z - min_z][cube.x - min_x][cube.y - min_y] = State.Active
    return cubes


def run_cycle(cubes):
    cubes_to_search = set()
    for i in range(len(cubes)):
        for j in range(len(cubes[0])):
            for k in range(len(cubes[0][0])):
                cube = Cube(j, k, i)
                neighbors = get_neighbors(cube)
                cubes_to_search.add(cube)
                cubes_to_search = cubes_to_search.union(set(neighbors))

    cube_to_active = defaultdict(lambda: set())
    for cube in cubes_to_search:
        neighbors = get_neighbors(cube)
        for nbr in neighbors:
            if cube.is_active(cubes):
                cube_to_active[nbr].add(cube)
            if nbr.is_active(cubes):
                cube_to_active[cube].add(nbr)

    def should_be_active(pair):
        cube, active_neighbors = pair
        n_count = len(active_neighbors)
        is_active = cube.is_active(cubes)
        if is_active:
            return n_count == 2 or n_count == 3
        else:
            return n_count == 3

    cubes_to_make_active = list(
        map(
            lambda x: x[0],
            filter(should_be_active, cube_to_active.items())
        )
    )

    return next_state(cubes_to_make_active)


def print_cubes(cubes):
    for layer in range(len(cubes)):
        print(f"z={layer - len(cubes) // 2}")
        for row in cubes[layer]:
            joined = "".join(map(lambda x: str(x), row))
            print(joined)
        print()


def part_one(lines: str):
    init_state = [parse_input(lines)]
    cubes = init_state

    # print("Before any cycles:")
    # print()
    # print_cubes(cubes)

    for i in range(6):
        cubes = run_cycle(cubes)
        # print(f"After {i + 1} cycle:")
        # print()
        # print_cubes(cubes)


    count = 0
    for layer in cubes:
        for row in layer:
            for cube in row:
                if cube == State.Active:
                    count += 1
    return count


def next_hstate(cubes_to_make_active):
    max_x = max(cubes_to_make_active, key=lambda cube: cube.x).x
    min_x = min(cubes_to_make_active, key=lambda cube: cube.x).x
    max_y = max(cubes_to_make_active, key=lambda cube: cube.y).y
    min_y = min(cubes_to_make_active, key=lambda cube: cube.y).y
    max_z = max(cubes_to_make_active, key=lambda cube: cube.z).z
    min_z = min(cubes_to_make_active, key=lambda cube: cube.z).z
    max_w = max(cubes_to_make_active, key=lambda cube: cube.w).w
    min_w = min(cubes_to_make_active, key=lambda cube: cube.w).w

    len_x = max_x - min_x + 1
    len_y = max_y - min_y + 1
    len_z = max_z - min_z + 1
    len_w = max_w - min_w + 1

    cubes = [
        [
            [
                [
                    State.Inactive for _ in range(len_y)
                ] for _ in range(len_x)
            ] for _ in range(len_z)
        ] for _ in range(len_w)
    ]

    for cube in cubes_to_make_active:
        cubes[cube.w - min_w][cube.z - min_z][cube.x - min_x][cube.y - min_y] = State.Active
    return cubes


def run_hcycle(cubes):
    cubes_to_search = set()
    for w in range(len(cubes)):
        for z in range(len(cubes[0])):
            for x in range(len(cubes[0][0])):
                for y in range(len(cubes[0][0][0])):
                    cube = HCube(x, y, z, w)
                    neighbors = get_hneighbors(cube)
                    cubes_to_search.add(cube)
                    cubes_to_search = cubes_to_search.union(set(neighbors))

    cube_to_active = defaultdict(lambda: set())
    for cube in cubes_to_search:
        neighbors = get_hneighbors(cube)
        for nbr in neighbors:
            if cube.is_active(cubes):
                cube_to_active[nbr].add(cube)
            if nbr.is_active(cubes):
                cube_to_active[cube].add(nbr)

    def should_be_active(pair):
        cube, active_neighbors = pair
        n_count = len(active_neighbors)
        is_active = cube.is_active(cubes)
        if is_active:
            return n_count == 2 or n_count == 3
        else:
            return n_count == 3

    cubes_to_make_active = list(
        map(
            lambda x: x[0],
            filter(should_be_active, cube_to_active.items())
        )
    )

    return next_hstate(cubes_to_make_active)


def get_hneighbors(cube: HCube):
    neighbors = []
    for i in (0, -1, 1):
        for j in (0, -1, 1):
            for k in (0, -1, 1):
                for l in (0, -1, 1):
                    neighbor = HCube(
                        cube.x + i,
                        cube.y + j,
                        cube.z + k,
                        cube.w + l,
                    )
                    if neighbor == cube:
                        continue
                    neighbors.append(neighbor)
    return neighbors


def part_two(lines: str):
    init_state = [[parse_input(lines)]]
    cubes = init_state

    # print("Before any cycles:")
    # print()
    # print_cubes(cubes)

    for i in range(6):
        cubes = run_hcycle(cubes)
        # print(f"After {i + 1} cycle:")
        # print()
        # print_cubes(cubes)


    count = 0
    for idk in cubes:
        for layer in idk:
            for row in layer:
                for cube in row:
                    if cube == State.Active:
                        count += 1
    return count


def main():
    lines = Path(Path(__file__).parent, "2020_d17.txt").read_text()
    print(f"part 1 solution: {part_one(lines)}")
    print(f"part 2 solution: {part_two(lines)}")


if __name__ == '__main__':
    main()
