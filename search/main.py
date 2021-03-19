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
from search.graph import to_graph

def main():
    try:
        with open(sys.argv[1]) as file:
            data = json.load(file)
    except IndexError:
        print("usage: python3 -m search path/to/input.json", file=sys.stderr)
        sys.exit(1)

    matches = matchups(data)
    board = reformat_board(data)
    graphs = to_graph(board)
    print(board)
    turn = 0
    while not game_over(matches):
        moves_list = []
        for graph in graphs:
            print(matches[graph.root.token][0])
            path = graph.iterative_DS(matches[graph.root.token][0])
            moves_list.append(path)
            matches[graph.root.token][1] = max(0, matches[graph.root.token][1] - 1)
        for move in zip(moves_list):
            turn += 1
            for i in range(len(move)):
                r_a, p_a = graphs[i].root.position
                r_b, p_b = round[i].position
                print_slide(turn, r_a, p_a, r_b, p_b)
                graph[i].move_root(round[i])

    # TODO:
    # Find and print a solution to the board configuration described
    # by `data`.
    # Why not start by trying to print this configuration out using the
    # `print_board` helper function? (See the `util.py` source code for
    # usage information).
