from functools import reduce
from pathlib import Path


def get_item_priority(letter: str):
    if letter.islower():
        return ord(letter) - ord("a") + 1
    return ord(letter) - ord("A") + 27


def part_one(lines: str):
    rucksacks = lines.split()

    priorities = []
    for rs in rucksacks:
        middle = len(rs) // 2

        seen = set()
        for item in rs[:middle]:
            seen.add(item)

        for item in rs[middle:]:
            if item in seen:
                priority = get_item_priority(item)
                priorities.append((item, priority))
                break

    def sum_priority(prev, curr):
        return prev + curr[1]

    return reduce(sum_priority, priorities, 0)


def alphabet_set():
    seen = set([ascii_val for ascii_val in range(ord('a'), ord('z') + 1)])
    seen = seen.union(set([ascii_val for ascii_val in range(ord('A'), ord('Z') + 1)]))
    return seen


def part_two(lines: str):
    rucksacks = lines.split()

    priorities = [alphabet_set() for _ in range(len(rucksacks) // 3)]
    for i, rs in enumerate(rucksacks):
        letters = set([ord(letter) for letter in rs])
        priorities[i // 3] = priorities[i // 3].intersection(letters)

    values = list(map(lambda x: get_item_priority(chr(x.pop())), priorities))
    return sum(values)


def main():
    file = Path("day_03.txt")
    lines = file.read_text()
    print(f"part 1 solution: {part_one(lines)}")
    print(f"part 2 solution: {part_two(lines)}")


if __name__ == '__main__':
    main()
