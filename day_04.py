import re
from dataclasses import dataclass
from pathlib import Path


PATTERN = re.compile(r"(\d+)-(\d+),(\d+)-(\d+)")


@dataclass()
class Range:
    start: int
    stop: int


def parse_input(lines: str):
    split_lines = lines.split()

    def mapper(line):
        match = PATTERN.search(line)
        return (
            Range(int(match.group(1)), int(match.group(2))),
            Range(int(match.group(3)), int(match.group(4))),
        )

    return list(map(mapper, split_lines))


def part_one(lines: str):
    parsed = parse_input(lines)
    count = 0
    for line in parsed:
        range1, range2 = line
        if range1.start <= range2.start and range1.stop >= range2.stop:
            count += 1
        elif range1.start >= range2.start and range1.stop <= range2.stop:
            count += 1
    return count


def part_two(lines: str):
    parsed = parse_input(lines)
    count = 0
    for line in parsed:
        range1, range2 = line
        if range1.start <= range2.stop and range1.stop >= range2.start:
            count += 1
        elif range2.start <= range1.stop and range2.stop >= range1.start:
            count += 1
    return count


def main():
    file = Path("day_04.txt")
    lines = file.read_text()
    print(f"part 1 solution: {part_one(lines)}")
    print(f"part 2 solution: {part_two(lines)}")


if __name__ == '__main__':
    main()
