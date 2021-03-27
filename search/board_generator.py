from itertools import product
from queue import Queue

COUNTER = {"R" : "s", "P": "r", "S": "p"}
boards_made = []
boards_considered = [0]
# Applies a list of moves for each piece to the board. Assumes that in one turn, you can move one or more pieces
# We greedily assume that there will never be two pieces of different type on the same tile
# If we have two of the same piece on the same tile, should work fine
def apply_turn(node, moves):
    boards_considered[0] += 1
    # Invalidates boards where upper pieces move on to the same tile
    if len(set([move[1] for move in moves])) < len(moves):
        return False

    new_board = node.boardstate.copy()
    for curr_pos, new_pos in moves:
        piece = new_board[curr_pos]

        # Invalidates boards where an upper piece destroys itself
        if new_pos in new_board and new_board[new_pos].islower() and \
        new_board[new_pos] != COUNTER[piece]:
            return False

        del new_board[curr_pos]
        new_board[new_pos] = piece

    #Invalidates boards that have already been created since revisiting the board
    #is weakly inferior (at most as optimal)
    if new_board in boards_made:
        return False


    boards_made.append(new_board)
    return new_board

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
            adjacent_states.append(new_board)
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
            move_list.remove(position)
            swing_moves = swing_moves + move_list
    return swing_moves

def get_slide_moves(position, board):
    """
    Given a current position and board state get all possible slide moves
    the token moves to an adjacent tile, remains on the board and does not move
    onto a block
    """
    r,q = position
    blocks = [rq for rq in board if board[rq] == "B"]
    ran = range(-4,5)
    return [(r+i, q+j) for i in [-1,0,1] for j in [-1,0,1]
            if i != j and r+i in ran and q+j in ran and \
            -(r+i)-(q+j) in ran and (r+i, q+j) not in blocks]

board_graph = {}
def initialise_board(board):
    for r in range(-4,5):
        for q in range(-4,5):
            if -r-q in range(-4,5):
                board_graph[(r,q)] = get_slide_moves((r,q), board)

def distance(p1, p2):
    Q = Queue()
    Q.put((p1, 0))
    explored = []
    while True:
        tile, cost = Q.get()
        for adj_tile in board_graph[tile]:
            if adj_tile == p2:
                return cost + 1
            if adj_tile not in explored:
                explored.append(adj_tile)
                Q.put((adj_tile, cost + 1))
