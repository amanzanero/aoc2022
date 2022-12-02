from enum import Enum
from pathlib import Path


class Result(Enum):
    LOSE = 2
    DRAW = 1
    WIN = 0


OPPONENT_CHOICES = ["A", "B", "C"]

MY_CHOICES = ["X", "Y", "Z"]

SCORE = {
    "A": ["Y", "X", "Z"],
    "B": ["Z", "Y", "X"],
    "C": ["X", "Z", "Y"],
}

SCORE_2 = {
    "A": ["C", "A", "B"],
    "B": ["A", "B", "C"],
    "C": ["B", "C", "A"],
}


def part_one(lines: str):
    score = 0
    for line in lines.split("\n"):
        opp, me = line.split()
        i = SCORE[opp].index(me)
        if i == Result.LOSE.value:
            score += 0
        elif i == Result.DRAW.value:
            score += 3
        else:
            score += 6

        if me == "X":
            score += 1
        elif me == "Y":
            score += 2
        else:
            score += 3
    print(f"solution 1: {score}")


def part_two(lines: str):
    score = 0
    for line in lines.split("\n"):
        opp, me = line.split()
        i = MY_CHOICES.index(me)
        my_option = SCORE_2[opp][i]

        if i == 0:
            score += 0
        elif i == 1:
            score += 3
        else:
            score += 6

        if my_option == "A":
            score += 1
        elif my_option == "B":
            score += 2
        else:
            score += 3
    print(f"solution 2: {score}")


def main():
    file = Path("day_02.txt")
    lines = file.read_text()
    part_one(lines)
    part_two(lines)


if __name__ == '__main__':
    main()
