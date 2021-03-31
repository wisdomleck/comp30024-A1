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
from search.util import print_board, print_slide, print_swing, reformat_board
from search.graph import Node, Graph
from search.search import search

def main():
    try:
        with open(sys.argv[1]) as file:
            data = json.load(file)
    except IndexError:
        print("usage: python3 -m search path/to/input.json", file=sys.stderr)
        sys.exit(1)

    # TEST IF BOARD MOVE WORKS
    firstNode = Node(reformat_board(data), 0, [])
    graph = Graph(firstNode)

    solution = search(graph)
    path = []
    while solution:
        path.insert(0,solution)
        solution = solution.predecessor

    for node in path:
        for p, q in node.moveset:
            if node.distance(p, q) == 1:
                print_slide(node.depth, p[0], p[1], q[0], q[1])
            elif node.distance(p,q) == 2:
                print_swing(node.depth, p[0], p[1], q[0], q[1])
