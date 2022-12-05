import re
from dataclasses import dataclass
from pathlib import Path

CRATE_PATTERN = re.compile(r"(\s{3}\s?)|\[([A-z])]\s?")
INSTRUCTION_PATTERN = re.compile(r"move (\d+) from (\d+) to (\d+)")


@dataclass()
class Instruction:
    quantity: int
    position: int
    destination: int


def parse_input(lines: str):
    lines_list = lines.split("\n")
    end_of_block = lines_list.index("")
    columns = end_of_block - 1

    stacks = []

    for line in lines_list[:columns]:
        matches = CRATE_PATTERN.findall(line)
        for i, match in enumerate(matches):
            if len(stacks) < i + 1:
                stacks.append([])
            if len(match[1]):
                stacks[i].append(match[1])

    instructions = []
    for line in lines_list[end_of_block+1:]:
        match = INSTRUCTION_PATTERN.search(line)
        instructions.append(
            Instruction(
                int(match.group(1)),
                int(match.group(2)) - 1,
                int(match.group(3)) - 1,
            )
        )
    return [stack[::-1] for stack in stacks], instructions


def part_one(lines: str):
    stacks, instructions = parse_input(lines)

    for i, instruction in enumerate(instructions):
        for _ in range(instruction.quantity):
            pop = stacks[instruction.position].pop()
            if pop:
                stacks[instruction.destination].append(pop)

    return "".join(
        map(lambda x: x[-1], stacks)
    )


def part_two(lines: str):
    stacks, instructions = parse_input(lines)

    for i, instruction in enumerate(instructions):
        lift = []
        for _ in range(instruction.quantity):
            pop = stacks[instruction.position].pop()
            lift.append(pop)
        stacks[instruction.destination].extend(lift[::-1])

    return "".join(
        map(lambda x: x[-1], stacks)
    )


def main():
    file = Path("day_05.txt")
    lines = file.read_text()
    print(f"part 1 solution: {part_one(lines)}")
    print(f"part 2 solution: {part_two(lines)}")


if __name__ == '__main__':
    main()
