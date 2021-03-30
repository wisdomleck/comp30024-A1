from itertools import product
from queue import Queue
from search.util import print_board

COUNTER = {"R" : "s", "P": "r", "S": "p"}
ALLIED_PIECES = ["R", "P", "S"]
boards_made = []
boards_considered = [0]

# Applies a list of moves for each piece to the board. Assumes that in one turn, you can move one or more pieces
# We greedily assume that there will never be two pieces of different type on the same tile
# If we have two of the same piece on the same tile, should work fine
def apply_turn(node, moves):
    boards_considered[0] += 1
    # Invalidates boards where upper pieces move on to the same tile
    new_positions = [move[1] for move in moves]
    if len(set(new_positions)) < len(moves):
        return False

    new_board = node.boardstate.copy()
    for curr_pos, new_pos in moves:
        piece = node.boardstate[curr_pos]

        # Invalidates boards where an upper piece destroys itself
        if new_pos in new_board and node.boardstate[new_pos].islower() and \
        new_board[new_pos] != COUNTER[piece]:
            return False

        if curr_pos not in new_positions:
            del new_board[curr_pos]
        new_board[new_pos] = piece

    #Invalidates boards that have already been created since revisiting the board
    #is weakly inferior (at most as optimal)
    #if new_board in boards_made:
    #    return False

    for board in boards_made:
        if equals(board, new_board):
            #print_board(board)

            #print_board(new_board)
            return False
    boards_made.append(new_board)
    return new_board

def equals(board1, board2):
    rel_pieces = []
    for key, value in board1.items():
        if value in COUNTER.keys() and COUNTER[value] in board1.values():
            rel_pieces.append((key, value))

    num_same = 0
    for p, q in rel_pieces:
        if (p,q) in board2.items():
            num_same += 1
    return num_same == len(rel_pieces)

def generate_adjacents(node):
    """
    Generates a list of all adjacent nodes to the argument, where adjacency is
    defined by all nodes whose board states can be reached with one move in the
    current baord state.
    """
    # Makes a dictionary where keys are current upper token positions and
    # values are the list of positions attainable from one slide move
    slide_moves = {}
    for key, value in node.boardstate.items():
        if value.isupper() and value != "B":
            slide_moves[key] = get_slide_moves(key, node.boardstate)

    # Append list of swing moves to get all moves
    moves_dict = {}
    #relevant_pieces = [name ]
    for key in slide_moves:
        all_moves = set(slide_moves[key] + get_swing_moves(key, slide_moves))
        moves_dict[key] = list(all_moves)

    # Convert from dictionary to list of list of tuples of the form:
    #[[(curr_move, next_move)...]...] where each tokens moves occupy a list
    moves_list = []
    for curr, news in moves_dict.items():
        moves_list.append([(curr, new) for new in news])

    # Get all combinations of moves and for each combo construct a new board state
    adjacent_states = []
    turns = list(product(*moves_list))

    for turn in turns:
        new_board = apply_turn(node, turn)
        if new_board:
            adjacent_states.append((turn, new_board))
    return adjacent_states


def get_swing_moves(position, slide_moves):
    """
    Given a current position and a dictionary of slide moves, if the current
    position of a token is in the slide move of another token these two must
    be adjacent and their slide moves must constitute the others possible swing
    moves
    """
    swing_moves = []
    for move_list in slide_moves.values():
        if position in move_list:
            swing_moves += can_swing_to(position, move_list)
    return swing_moves

def can_swing_to(mover, positions):
    clusters = []
    positions_copy = positions.copy()
    while positions_copy:
        prev_cluster = [positions_copy.pop()]
        new_cluster = clustering(prev_cluster, positions_copy)
        while len(prev_cluster) < len(new_cluster):
            positions_copy = list(set(positions_copy).difference(set(new_cluster)))
            prev_cluster = new_cluster
            new_cluster = clustering(prev_cluster, positions_copy)
        clusters.append(new_cluster)

    for cluster in clusters:
        if mover in cluster:
            cluster.remove(mover)
            return cluster
    return []

def clustering(cluster, positions):
    cluster_copy = cluster.copy()
    for p in cluster:
        for q in positions:
            if q in get_adjacents(p):
                cluster_copy.append(q)
    return cluster_copy

def get_slide_moves(position, board):
    """
    Given a current position and board state get all possible slide moves
    the token moves to an adjacent tile, remains on the board and does not move
    onto a block
    """
    r,q = position
    blocks = [p for p in board if board[p] == "B"]
    ran = range(-4,5)
    return [p for p in get_adjacents(position) if p not in blocks]

def get_adjacents(position):
    r,q = position
    ran = range(-4,5)
    return [(r+i, q+j) for i in [-1,0,1] for j in [-1,0,1]
            if i != j and r+i in ran and q+j in ran and -(r+i)-(q+j) in ran]
