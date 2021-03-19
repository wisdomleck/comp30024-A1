""" This file contains class definitions that we will use to represent the game
as a set of states/nodes in a graph. Some definitions here are useful to represent
possible coordinates on the board, or possible moves """

""" Directions that a piece can move """
MOVES = [(0,-1), (0, 1), (1,-1), (1,0), (-1,0), (-1,-1)]

""" Valid squares on the board. Relevant since the board isn't square """
TILES =    [(4, -4), (4, -3), (4, -2), (4, -1), (4, 0),
        (3, -4), (3, -3), (3, -2), (3, -1), (3, 0), (3, 1),
      (2, -4), (2, -3), (2, -2), (2, -1), (2, 0), (2, 1), (2, 2),
   (1, -4), (1, -3), (1, -2), (1, -1), (1, 0), (1, 1), (1, 2), (1, 3),
(0, -4), (0, -3), (0, -2), (0, -1), (0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
   (-1, -3), (-1, -2), (-1, -1), (-1, 0), (-1, 1), (-1, 2), (-1, 3), (-1, 4),
      (-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2), (-2, 3), (-2, 4),
        (-3, -1), (-3, 0), (-3, 1), (-3, 2), (-3, 3), (-3, 4),
            (-4, 0), (-4, 1), (-4, 2), (-4, 3), (-4, 4)]

class Move:
    def __init__(self, t, r_a, q_a, r_b, q_b):

""" Initialise a graph by passing in a root node. This node then
will store edges out to other nodes """
class Graph:
    def __init__(self, initial_state):
        self.initial_state = initial_state



""" Node in a graph to represent the current board state. Might need to update later with
edge weights, for now just keep track of the depth """

class Node:
    def __init__(self, boardstate, depth):
        self.boardstate = boardstate
        self.adj_list = []
        self.depth = depth

    # Fill in this node with a list of adjacent nodes, generated from moving pieces
    def add_neighbours(self, newnodes):
        self.adj_list = newnodes

    # Might be useful when making a new, branching node
    def get_depth(self):
        return self.depth

    # Returns list of enemy (lower) pieces
    def get_enemy_pieces(self):
        pieces_left = []
        for key, value in self.boardstate:
            if value == "p" or value == "r" or value == "s":
                pieces_left.append(value)
        return pieces_left

    # Returns number of enemy (lower pieces left)
    def enemy_pieces_left(self):
        return len(get_enemy_pieces(self))

    # Returns whether the game is in a won state given by the rules
    def won_state(self):
        return

    def apply_move(self, move1, move2 = None, move3 = None):
