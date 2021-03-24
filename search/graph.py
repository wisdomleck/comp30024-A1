""" This file contains class definitions that we will use to represent the game
as a set of states/nodes in a graph. Some definitions here are useful to represent
possible coordinates on the board, or possible moves """

from search.board_generator import generate_adjacents

# Uninitialised value for distance in heuristic
BIGDIST = 1000000
COUNTER = {"R" : "s", "P": "r", "S": "p"}
ALLIED_PIECES = ["R", "S", "P"]

""" Initialise a graph by passing in a root node. This node then
will store edges out to other nodes """
class Graph:
    def __init__(self, initial_state):
        self.initial_state = initial_state
    def __init__(self, root):
        self.root = root


""" Node in a graph to represent the current board state. Might need to update later with
edge weights, for now just keep track of the depth """

class Node:
    def __init__(self, boardstate, depth):
        self.boardstate = boardstate
        self.predecessor = None
        # Implicitly tells us which move it is?
        self.depth = depth
        #self.adjacent_generator = BoardGenerator(self)
        #self.adj_list = []

    def __lt__(self, other):
        f1 = self.depth + self.give_heuristic_value()
        f2 = other.depth + other.give_heuristic_value()
        return f1 < f2

    def adjacents(self):
        boards = generate_adjacents(self)
        for board in boards:
            yield Node(board, self.depth + 1)

    # Might be useful when making a new, branching node
    def get_depth(self):
        return self.depth

    # Returns list of enemy (lower) pieces
    def get_enemy_pieces(self):
        pieces_left = []
        for key, value in (self.boardstate).items():
            if value == "p" or value == "r" or value == "s":
                pieces_left.append(value)
        return pieces_left

    # Returns number of enemy (lower pieces left)
    def enemy_pieces_left(self):
        return len(self.get_enemy_pieces())

    # Returns whether the game is in a won state given by the rules
    # Won state if the other player has 0 tokens, or if we have invincible token and other player has 1 token not invincible
    # But for Part A, we win if and only if the lower player has 0 tokens left
    def won_state(self):
        return len(self.get_enemy_pieces()) == 0


    # Calculates the manhattan distance from two tiles on the hexagonal board
    def distance(self, coord1, coord2):
        (r1, c1) = coord1
        (r2, c2) = coord2

        dr = r1 - r2
        dc = c1 - c2
        if (dr < 0 and dc < 0) or (dr > 0 and dc > 0):
            return abs(dr + dc)
        else:
            return max(abs(dr), abs(dc))

    # TEST
    # calculate the minimum distance from an instance of piece to its closest piece it can eat
    def min_distance(self, coord, piece_type):
        mindist = BIGDIST
        for key, value in (self.boardstate).items():
            if value == COUNTER[piece_type]:
                if self.distance(coord, key) < mindist:
                    mindist = self.distance(coord, key)
        return mindist

    # test this
    def give_heuristic_value(self):
        heuristic = 0
        # for each allied piece, calculate the min distance to each piece it can eat. if not there, then assign 0
        for key, value in (self.boardstate).items():
            if value in ALLIED_PIECES:
                if COUNTER[value] in self.get_enemy_pieces():
                    heuristic += self.min_distance(key, value)
                else:
                    continue
        return heuristic
