"""
COMP30024 Artificial Intelligence, Semester 1, 2021
Project Part A: Searching

This script contains the entry point to the program (the code in
`__main__.py` calls `main()`). Your solution starts here!
"""

import sys
import json

# If you want to separate your code into separate files, put them
# inside the `search` directory (like this one and `util.py`) and
# then import from them like this:
from search.util import print_board, print_slide, print_swing, reformat_board, matchups, game_over
from search.graph import Node, Move

def main():
    try:
        with open(sys.argv[1]) as file:
            data = json.load(file)
    except IndexError:
        print("usage: python3 -m search path/to/input.json", file=sys.stderr)
        sys.exit(1)

    # TEST IF BOARD MOVE WORKS
    firstNode = Node(reformat_board(data), 0)
    print_board(firstNode.boardstate)
    print(firstNode.boardstate)

    # Move the scissor piece one square to the right
    move1 = Move(1, 0, 3, 0, 4)
    nextNode = firstNode.apply_turn([move1])
    print_board(nextNode.boardstate)
    print(nextNode.boardstate)

    # TODO:
    # Find and print a solution to the board configuration described
    # by `data`.
    # Why not start by trying to print this configuration out using the
    # `print_board` helper function? (See the `util.py` source code for
    # usage information).
