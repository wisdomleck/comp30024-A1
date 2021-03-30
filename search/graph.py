""" This file contains class definitions that we will use to represent the game
as a set of states/nodes in a graph. Some definitions here are useful to represent
possible coordinates on the board, or possible moves """

from search.board_generator import generate_adjacents
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


""" Node in a graph to represent the current board state. Might need to update later with
edge weights, for now just keep track of the depth """

class Node:
    def __init__(self, boardstate, depth, moveset):
        self.boardstate = boardstate
        self.predecessor = None
        # Implicitly tells us which move it is?
        self.depth = depth
        self.moveset = moveset
        #self.adjacent_generator = BoardGenerator(self)
        #self.adj_list = []

    def __lt__(self, other):
        f1 =  self.get_min_distances() + 10*self.enemy_pieces_left() - 0.33*self.dist_to_blocks()
        f2 =  other.get_min_distances() + 10*other.enemy_pieces_left() - 0.33*other.dist_to_blocks()
        return f1 < f2

    def adjacents(self):
        boards = generate_adjacents(self)
        for moveset, board in boards:
            yield Node(board, self.depth + 1, moveset)

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
    def board_score(self):
        ally_dist_sum = 0
        for key, value in self.boardstate.items():
            if value in ALLIED_PIECES:
                for key1, value1 in self.boardstate.items():
                    if value1 in ALLIED_PIECES:
                        ally_dist_sum += self.distance(key, key1)

        ally_dist_sum /= 2
        enemy_dist_sum = 0
        for key,value in self.boardstate.items():
            if value in ALLIED_PIECES:
                for key1, value1 in self.boardstate.items():
                    if COUNTER[value] == value1:
                        enemy_dist_sum += self.distance(key, key1)

        return ally_dist_sum + enemy_dist_sum

    def distance(self, coord1, coord2):
        (r1, c1) = coord1
        (r2, c2) = coord2

        dr = r1 - r2
        dc = c1 - c2
        if (dr < 0 and dc < 0) or (dr > 0 and dc > 0):
            return abs(dr + dc)
        else:
            return max(abs(dr), abs(dc))

    def heuristic(self):
        # Find the shortest distance between enemy pieces + shortest distance of an allied piece to enemy piece
        piece_heuristics = []
        # Find the shortest path to each piece
        for piece in ALLIED_PIECES:
            # Find tiles of enemies
            enemy_tiles = []
            ally_tiles = []
            for key, value in self.boardstate.items():
                if value == piece:
                    ally_tiles.append(key)
                if value == COUNTER[piece]:
                    enemy_tiles.append(key)

            # Generate all permutations, find the minimum distance pathway through them
            # If no enemy tiles, then go to next piece
            if len(enemy_tiles) == 0:
                continue

            mindist = 10000;
            for ally in ally_tiles:
                perms = list(permutations(enemy_tiles))
                for path in perms:
                    path = list(path)
                    path.insert(0, ally)
                    dist = 0
                    #print(path)
                    for i in range(len(path)-1):
                        dist += self.distance(path[i], path[i+1])
                    if dist < mindist:
                        mindist = dist

            piece_heuristics.append((mindist))
        if len(piece_heuristics) == 0:
            return 0

        return max(piece_heuristics)


    ###################################################################################################################################
    def get_min_distances(self):
        allied_piece_tiles = []
        #get coords of allied pieces
        for key, value in self.boardstate.items():
            if value in ALLIED_PIECES:
                allied_piece_tiles.append(key)

        # find mindist of each piece to enemy piece
        mindist = 0
        mindist_total = 0
        for tile in allied_piece_tiles:
            if COUNTER[self.boardstate[tile]] in self.boardstate.values():
                mindist = 100000
                # then we have an enemy piece
                for key, value in self.boardstate.items():
                    if value == COUNTER[self.boardstate[tile]]:
                        dist = self.distance(key, tile)
                        if dist < mindist:
                            mindist = dist
            mindist_total += mindist

        return mindist_total


    ##### STill got some tiebreaks that don't make sense
    def get_dist_to_all_enemies(self):
        allied_piece_tiles = []
        #get coords of allied pieces
        for key, value in self.boardstate.items():
            if value in ALLIED_PIECES:
                allied_piece_tiles.append(key)

        totaldist = 0
        for tile in allied_piece_tiles:
            if COUNTER[self.boardstate[tile]] in self.boardstate.values():
                # then we have an enemy piece
                for key, value in self.boardstate.items():
                    if value == COUNTER[self.boardstate[tile]]:
                        dist = self.distance(key, tile)
                        totaldist += dist

        if totaldist == 0:
            return 0
        else:
            return 1/totaldist


    ##### STill got some tiebreaks that don't make sense
    ## reward allies to stay close to eachother when tiebreaking?
    def get_dist_to_all_allies(self):
        allied_piece_tiles = []
        #get coords of allied pieces
        for key, value in self.boardstate.items():
            if value in ALLIED_PIECES:
                allied_piece_tiles.append(key)

        totaldist = 0

        for i in range(len(allied_piece_tiles)-1):
            totaldist += self.distance(allied_piece_tiles[i], allied_piece_tiles[i+1])


        if totaldist == 0:
            return 0
        else:
            return 1/totaldist

    # We want to be near as many adjacent blocks?
    def dist_to_blocks(self):
        allied_piece_tiles = []
        block_piece_tiles = []
        #get coords of allied pieces
        for key, value in self.boardstate.items():
            if value in ALLIED_PIECES:
                allied_piece_tiles.append(key)
            if value == 'B':
                block_piece_tiles.append(key)

        score = 0
        for ally in allied_piece_tiles:
            for block in block_piece_tiles:
                if self.distance(ally, block) == 1:
                    score += 1
        return score
