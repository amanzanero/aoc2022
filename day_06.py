from pathlib import Path


def part_one(lines: str):
    tail, head = 0, 4
    while len(set(list(lines[tail:head]))) != 4:
        tail += 1
        head += 1
    return head


def part_two(lines: str):
    tail, head = 0, 14
    while len(set(list(lines[tail:head]))) != 14:
        tail += 1
        head += 1
    return head


def main():
    file = Path("day_06.txt")
    lines = file.read_text()
    print(f"part 1 solution: {part_one(lines)}")
    print(f"part 2 solution: {part_two(lines)}")


if __name__ == '__main__':
    main()
