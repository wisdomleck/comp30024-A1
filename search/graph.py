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



""" Defines a move class. Turn, (r,q) source, (r,q) dest. Assumes the move
is valid """
class Move:
    def __init__(self, r_a, q_a, r_b, q_b):
        self.from_r = r_a
        self.from_q = q_a
        self.to_r = r_b
        self.to_q = q_b


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
        # Implicitly tells us which move it is?
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
        return len(self.get_enemy_pieces())

    # Returns whether the game is in a won state given by the rules
    # Won state if the other player has 0 tokens, or if we have invincible token and other player has 1 token not invincible
    # But for Part A, we win if and only if the lower player has 0 tokens left
    def won_state(self):
        return len(self.get_enemy_pieces()) == 0

    # redo this
    # Applies a given move for a single piece to the board. Returns a new updated board dict
    # ASSUMES the move is valid. Ie the tile contains a piece that we control
    def apply_single_move(self, move):
        # copy the dictionary
        newboardstate = (self.boardstate).copy()

        (row, col) = (move.from_r, move.from_q)
        (newrow, newcol) = (move.to_r, move.to_q)
        piece = (self.boardstate)[(row,col)]

        # Moving a piece means the old coord no longer is occupied
        del (newboardstate)[(row, col)]

        # The new tile moves to occupies the piece now
        newboardstate[(newrow, newcol)] = piece

        return newboardstate

    # Applies a list of moves for each piece to the board. Assumes that in one turn, you can move one or more pieces
    # We greedily assume that there will never be two pieces of different type on the same tile
    # If we have two of the same piece on the same tile, should work fine
    def apply_turn(self, moves):
        newnode = Node(self.boardstate, self.depth + 1)
        for move in moves:
            newnode.boardstate = newnode.apply_single_move(move)
        return newnode
