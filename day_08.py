from pathlib import Path
from pprint import pp
from dataclasses import dataclass


def part_one(lines: str):
    lines_list = lines.split("\n")
    lines_list = [
        [
            int(number) for number in line
        ] for line in lines_list
    ]
    visible = set()
    len_row = len(lines_list[0])
    len_col = len(lines_list)
    # left to right
    for i in range(len_col):
        max_tree = lines_list[i][0]
        visible.add((i, 0))
        for j in range(1, len_row):
            if lines_list[i][j] > max_tree:
                max_tree = lines_list[i][j]
                visible.add((i, j))
    # right to left
    for i in range(len_col):
        max_tree = lines_list[i][len_row - 1]
        visible.add((i, len_row - 1))
        for j in range(len_row - 2, 0, -1):
            if lines_list[i][j] > max_tree:
                max_tree = lines_list[i][j]
                visible.add((i, j))
    # top to bottom
    for j in range(len_row):
        max_tree = lines_list[0][j]
        visible.add((0, j))
        for i in range(1, len_col):
            if lines_list[i][j] > max_tree:
                max_tree = lines_list[i][j]
                visible.add((i, j))
    # bottom to top
    for j in range(len_row):
        max_tree = lines_list[len_col - 1][j]
        visible.add((len_col - 1, j))
        for i in range(len_col - 2, 0, -1):
            if lines_list[i][j] > max_tree:
                max_tree = lines_list[i][j]
                visible.add((i, j))
    return len(visible)


@dataclass()
class Eave:
    top: int
    left: int
    bottom: int
    right: int


def part_two(lines: str):
    lines_list = lines.split("\n")
    lines_list = [[int(number) for number in line] for line in lines_list]

    memo = [[Eave(0, 0, 0, 0) for _ in range(len(lines_list))] for _ in range(len(lines_list))]
    for i in range(len(lines_list) - 1):
        for j in range(len(lines_list[0]) - 1):
            curr = lines_list[i][j]
            if i > 0:
                top = memo[i-1][j]
                tree = lines_list[i-1][j]
                if tree < curr:
                    memo[i][j].top += top.top + 1
                else:
                    memo[i][j].top = 1
            if j > 0:
                left = memo[i][j-1]
                tree = lines_list[i][j-1]
                if tree < curr:
                    memo[i][j].left += left.left + 1
                else:
                    memo[i][j].left = 1
    for i in range(len(lines_list) - 1, 0, -1):
        for j in range(len(lines_list[0]) - 1, 0, -1):
            curr = lines_list[i][j]
            if i < len(lines_list) - 1:
                bottom = memo[i+1][j]
                tree = lines_list[i+1][j]
                if tree < curr:
                    memo[i][j].bottom += bottom.bottom + 1
                else:
                    memo[i][j].bottom = 1
            if j < len(lines_list) - 1:
                right = memo[i][j+1]
                tree = lines_list[i][j+1]
                if tree < curr:
                    memo[i][j].right += right.right + 1
                else:
                    memo[i][j].right = 1
    scores = [
        [(e.left * e.right * e.top * e.bottom) for e in row] for row in memo
    ]
    ans = max([max(row) for row in scores])
    for i, row in enumerate(scores):
        found = False
        for j, val in enumerate(row):
            if val == ans:
                found = True
                break
        if found:
            break
    print(ans)
    print(i, j)
    print(memo[i][j])
    print(lines_list[i][j])
    return ans


def part_two_2(lines: str):
    lines_list = lines.split("\n")
    lines_list = [[int(number) for number in line] for line in lines_list]
    scores = [[0 for _ in range(len(lines_list))] for _ in range(len(lines_list))]
    for i in range(1, len(lines_list) - 2):
        for j in range(1, len(lines_list[0]) - 2):
            curr_max = lines_list[i][j]
            top_score = 1
            m = 1
            while i-m >= 0 and lines_list[i-m][j] < curr_max:
                top_score += 1
                curr_max = lines_list[i-m][j]
                m += 1

            curr_max = lines_list[i][j]
            bottom_score = 1
            m = 1
            while i+m < len(lines_list) and lines_list[i+m][j] < curr_max:
                bottom_score += 1
                curr_max = lines_list[i+m][j]
                m += 1

            curr_max = lines_list[i][j]
            left_score = 1
            m = 1
            while j-m >= 0 and lines_list[i][j-m] < curr_max:
                left_score += 1
                curr_max = lines_list[i][j-m]
                m += 1

            curr_max = lines_list[i][j]
            right_score = 1
            m = 1
            while j+m < len(lines_list) and lines_list[i][j+m] < curr_max:
                right_score += 1
                curr_max = lines_list[i][j+m]
                m += 1

            scores[i][j] = left_score * right_score * top_score * bottom_score
    return max([max(row) for row in scores])


def main():
    file = Path("day_08.txt")
    lines = file.read_text()
    print(f"part 1 solution: {part_one(lines)}")
    print(f"part 2 solution: {part_two(lines)}")
    print(f"part 2 solution: {part_two_2(lines)}")


if __name__ == '__main__':
    main()
