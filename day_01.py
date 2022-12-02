import heapq
from pathlib import Path


def part_one(lines: str):
    elf_cals = lines.split("\n")
    squashed = [0]
    current_elf = 0
    for index, cal in enumerate(elf_cals):
        if index == len(elf_cals) - 1:
            continue
        elif cal == "":
            squashed.append(0)
            current_elf += 1
        else:
            squashed[current_elf] += int(cal)

    solution = max(squashed)
    print(f"solution part 1: {solution}")
    return squashed


def part_two(lines):
    squashed = part_one(lines)
    queue = []
    for elf in squashed:
        heapq.heappush(queue, elf)
        if len(queue) > 3:
            heapq.heappop(queue)
    print(f"solution part 2: {sum(queue)}")


def main():
    file = Path("day_01.txt")
    input = file.read_text()
    part_one(input)
    part_two(input)


main()
