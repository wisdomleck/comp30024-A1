""" This file contains class definitions that we will use to represent the game
as a set of states/nodes in a graph. Some definitions here are useful to represent
possible coordinates on the board, or possible moves """

from search.board_generator import generate_adjacents, initialise_board, distance
from itertools import permutations
from math import ceil
# Uninitialised value for distance in heuristic
BIGDIST = 1000000
COUNTER = {"R" : "s", "P": "r", "S": "p"}
ALLIED_PIECES = ["R", "S", "P"]

""" Initialise a graph by passing in a root node. This node then
will store edges out to other nodes """
class Graph:
    def __init__(self, root):
        self.root = root
        initialise_board(root.boardstate)


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
        f1 = self.depth + self.give_heuristic_value5()
        f2 = other.depth + other.give_heuristic_value5()
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

    def generate_new_node(self, boardstate, depth):
        newnode = Node(boardstate, depth)
        return newnode
    # Returns whether the game is in a won state given by the rules
    # Won state if the other player has 0 tokens, or if we have invincible token and other player has 1 token not invincible
    # But for Part A, we win if and only if the lower player has 0 tokens left
    def won_state(self):
        return len(self.get_enemy_pieces()) == 0

    # Calculates the manhattan distance from two tiles on the hexagonal board
    """def distance(self, coord1, coord2):
        (r1, c1) = coord1
        (r2, c2) = coord2

        dr = r1 - r2
        dc = c1 - c2
        if (dr < 0 and dc < 0) or (dr > 0 and dc > 0):
            return abs(dr + dc)
        else:
            return max(abs(dr), abs(dc))"""

    ##################################### HEURISTIC 3 WORK #####################################

    # Gets upper and lower token matchings such that the lower pieces that
    # be captured by a given piece are grouped with that upper piece
    def matchings(self):
        # Iterates through lower pieces
        matches = {}
        for key, value in self.boardstate.items():
            if value.islower():
                closest_threat = None
                mindist = BIGDIST
                # Matches lowers pieces to the nearest upper piece that can capture
                # it. Stores the distance
                for key1, value1 in self.boardstate.items():
                    if value1 in COUNTER and COUNTER[value1] == value:
                        dist = distance(key, key1)
                        if dist  < mindist:
                            closest_threat = key1
                            mindist = dist
                #Distance is stores in a dictionary
                if closest_threat in matches:
                    matches[closest_threat].append(mindist)
                else:
                    matches[closest_threat] = [mindist]
        return matches

    # Heuristic for traversing graph
    def heuristic(self):
        # Gets the maximum distance needed to be travelled by a signle piece
        distances = [max(dist_list) for dist_list in self.matchings().values()]
        if distances:
            return max(distances)
        return 0
 
    def give_heuristic_value4(self):
        # Divide by number of terms to make heuristic admissable?
        distances = []
        total_heuristic = 0
        for piece in ALLIED_PIECES:
            piece_tiles = []

            # Get the tile coords of the allied piece type
            for key, value in (self.boardstate).items():
                if value == piece:
                    piece_tiles.append(key)

            distances.append(self.get_min_value_pairings(self.give_pairings_combos(piece, piece_tiles)))

        return max(distances)

        ##################################### HEURISTIC 5 WORK #####################################
    def give_heuristic_value5(self):
        # Find the shortest distance between enemy pieces + shortest distance of an allied piece to enemy piece
        piece_heuristics = []
        # Find the shortest path to each piece
        for piece in ALLIED_PIECES:
            mindist = 10000;
            # Find tiles of enemies
            enemy_tiles = []
            for key, value in self.boardstate.items():
                if value == COUNTER[piece]:
                    enemy_tiles.append(key)

            # Generate all permutations, find the minimum distance pathway through them
            # If no enemy tiles, then go to next piece
            if len(enemy_tiles) == 0:
                continue

            perms = list(permutations(enemy_tiles))
            for path in perms:
                dist = 0
                #print(path)
                for i in range(len(path)-1):
                    dist += self.distance(path[i], path[i+1])
                if dist < mindist:
                    mindist = dist

            # Now for the same piece, find the min dist to an enemy piece
            mindistpiece = 100000
            distpiece = 0
            for key, value in self.boardstate.items():
                if value == piece:
                    distpiece = self.min_distance(key, piece)
                    if distpiece < mindistpiece:
                        mindistpiece = distpiece

            # Get number of pieces of the current piece_type
            counter = 0
            for key, value in self.boardstate.items():
                if value == piece:
                    counter += 1

            # If we don't have any of the current allied piece, don't add to heuristic
            if counter == 0:
                continue

            piece_heuristics.append(ceil((mindist + mindistpiece)/counter))


        if len(piece_heuristics) == 0:
            return 0

        return max(piece_heuristics)
