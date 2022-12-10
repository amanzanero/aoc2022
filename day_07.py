from pathlib import Path
from dataclasses import dataclass
import heapq

max_size = 100000


@dataclass()
class MyNode:
    name: str
    dirs: set
    file_sum: int
    parent: any
    total_sum = None

    def __hash__(self):
        return hash(self.name)

    def __lt__(self, other):
        return self.total_sum < other.total_sum


def part_one(lines: str):
    lines_list = lines.split("\n")

    curr = MyNode(
        "/",
        set(),
        file_sum=0,
        parent=None
    )
    directories = {"/": curr}

    i = 0
    end = len(lines_list)
    while i < end:
        line = lines_list[i]
        if line.startswith("$"):
            args = line.split()
            cmd = args[1]
            if cmd == "cd":
                dir_arg = args[2]
                if dir_arg == "..":
                    curr = curr.parent
                elif dir_arg == "/":
                    curr = directories["/"]
                else:
                    new = MyNode(
                        dir_arg,
                        set(),
                        file_sum=0,
                        parent=curr
                    )
                    directories[dir_arg] = new
                    if new.parent:
                        new.parent.dirs.add(new)
                    curr = new
            elif cmd == "ls":
                # read lines until we get another command
                i += 1
                while i < end and not lines_list[i].startswith("$"):
                    if lines_list[i].startswith("dir"):
                        pass
                    else:
                        curr.file_sum += int(lines_list[i].split()[0])
                    i += 1
                i -= 1
        i += 1

    # now traverse the tree
    root = directories["/"]
    bingo = []

    def recursive_sum(node: MyNode):
        if len(node.dirs) == 0:
            total = node.file_sum
        else:
            dir_sums = 0
            for child in node.dirs:
                dir_sums += recursive_sum(child)
            total = node.file_sum + dir_sums

        if total < max_size:
            bingo.append(total)
        return total

    recursive_sum(root)
    return sum(bingo)


def part_two(lines: str):
    lines_list = lines.split("\n")

    curr = MyNode(
        "/",
        set(),
        file_sum=0,
        parent=None
    )
    directories = {"/": curr}

    i = 0
    end = len(lines_list)
    while i < end:
        line = lines_list[i]
        if line.startswith("$"):
            args = line.split()
            cmd = args[1]
            if cmd == "cd":
                dir_arg = args[2]
                if dir_arg == "..":
                    curr = curr.parent
                elif dir_arg == "/":
                    curr = directories["/"]
                else:
                    new = MyNode(
                        dir_arg,
                        set(),
                        file_sum=0,
                        parent=curr
                    )
                    directories[dir_arg] = new
                    if new.parent:
                        new.parent.dirs.add(new)
                    curr = new
            elif cmd == "ls":
                # read lines until we get another command
                i += 1
                while i < end and not lines_list[i].startswith("$"):
                    if lines_list[i].startswith("dir"):
                        pass
                    else:
                        curr.file_sum += int(lines_list[i].split()[0])
                    i += 1
                i -= 1
        i += 1

    # now traverse the tree
    root = directories["/"]
    hp = []

    def recursive_sum(node: MyNode):
        if len(node.dirs) == 0:
            total = node.file_sum
        else:
            dir_sums = 0
            for child in node.dirs:
                dir_sums += recursive_sum(child)
            total = node.file_sum + dir_sums
        node.total_sum = total
        heapq.heappush(hp, (total, node))
        return total
    total_size = recursive_sum(root)
    disk_size = 70000000
    min_needed = 30000000
    available = disk_size - total_size

    last = heapq.heappop(hp)
    while available + last[0] < min_needed:
        last = heapq.heappop(hp)
    print(last)
    return last[0]


def main():
    file = Path("day_07.txt")
    lines = file.read_text()
    print(f"part 1 solution: {part_one(lines)}")
    print(f"part 2 solution: {part_two(lines)}")


if __name__ == '__main__':
    main()
