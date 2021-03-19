def to_graph(board):
    roots = []
    nodes = {}
    ran = range(-4, +4+1)
    cells = [(r,q) for r in ran for q in ran if -r-q in ran]
    for rq in cells:
        if rq in board and board[rq] == "B":
            continue

        newNode = Node(rq)
        if rq in board:
            newNode.place_token(board[rq])
            print(board[rq])
            if board[rq].islower():
                roots.append(newNode)

        adjacents = [(rq[0], rq[1]-1), (rq[0]-1, rq[1]), (rq[0]-1, rq[1]+1)]
        for adj in adjacents:
            if adj in nodes:
                newNode.add_neighbour(nodes[adj])
        nodes[rq] = newNode

    graphs = []
    for root in roots:
        graphs.append(Graph(root))

    return graphs

class Graph:
    def __init__(self, root):
        self.root = root

    def move_root(self,neighbour):
        neighbour.token = self.root.token
        self.root.token = "E"
        self.root = neighbour

    def iterative_DS(self, target):
        i = 1
        while True:
            path = self.depth_first(self.root, target, i)
            i += 1
            if path:
                return path

    def depth_first(self, root, target, depth):
        if depth == 0:
            return False
        print(root.position)
        for adjacent in root.neighbours:
            if adjacent.token == target:
                return [adjacent]
            path = self.depth_first(adjacent, target, depth-1)
            if path:
                return path.append(adjacent)
        return False


class Node:
    def __init__(self, position):
        self.position = position
        self.token = None
        self.neighbours = []

    def add_neighbour(self, adjacent):
        self.neighbours.append(adjacent)
        adjacent.neighbours.append(self)

    def place_token(self, token):
        self.token = token
