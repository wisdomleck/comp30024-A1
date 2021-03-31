import heapq
from search.util import print_board
def a_star(graph):
    Q = [graph.root]
    heapq.heapify(Q)

    while Q:
        best_node = heapq.heappop(Q)
        if best_node.won_state():
            return best_node
        for node in best_node.adjacents():
            node.predecessor = best_node
            heapq.heappush(Q, node)


def iterative_depth_search(graph):
    """
    Applies an iterative depth search of graph representing the game, calling a
    depth first search on incrementally larger depths until a path to victory
    is found
    """
    i = 0
    path = False
    while not path:
        path = depth_first_search(graph.root, i)
        i += 1
    return path

def depth_first_search(root, depth):
    """
    Visits adjacent board states in a depth first traversal until a win state is
    found. When found, the path to the win state is returned.
    """
    if root.won_state():
        return [root]

    if depth == 0:
        return False

    if not root.adj_list:
        root.add_neighbours()

    for adjacent in root.adj_list:
        path = depth_first_search(adjacent, depth - 1)
        if path:
            path.insert(0, root)
            return path
    return False
