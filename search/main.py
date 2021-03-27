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
from search.graph import Node, Graph
from search.search import  iterative_depth_search, a_star
from search.board_generator import boards_made, boards_considered

def main():
    try:
        with open(sys.argv[1]) as file:
            data = json.load(file)
    except IndexError:
        print("usage: python3 -m search path/to/input.json", file=sys.stderr)
        sys.exit(1)

    # TEST IF BOARD MOVE WORKS
    firstNode = Node(reformat_board(data), 0)
    graph = Graph(firstNode)

    #solution_states = iterative_depth_search(graph)
    #for state in solution_states:
    #    print_board(state.boardstate)

    #print_board(firstNode.boardstate)
    #print("heuristic1:", firstNode.give_heuristic_value())
    #print("heuristic2:", firstNode.give_heuristic_value2()
    #print_board(firstNode.boardstate)
    #print(firstNode.give_heuristic_value2())
    solution = a_star(graph)
    path = []
    while solution:
        path.insert(0,solution)
        solution = solution.predecessor
    for node in path:
        print(node.heuristic())
        print_board(node.boardstate)

    print(f"boards considered: {boards_considered[0]}, boards made = {len(boards_made)}")

    #print_board(firstNode.boardstate)
    #print("heuristic:", firstNode.give_heuristic_value())

    # TODO:
    # Find and print a solution to the board configuration described
    # by `data`.
    # Why not start by trying to print this configuration out using the
    # `print_board` helper function? (See the `util.py` source code for
    # usage information).
