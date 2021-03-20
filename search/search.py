from itertools import product

def generate_adjacents(node):
    slide_moves = {}
    for key, value in node.board.items():
        if value.isupper() and value != "B":
            slide_moves[key] = slide_moves(key, node.board)

    all_moves_dict = {}
    for key in slide_moves:
        all_moves[key] = slide_moves[key] + swing_moves(key, slide_moves))

    all_moves_list = []
    for curr, news in all_moves_dict.items():
        all_moves_list.append([(curr new) for new in news])

    adjacent_nodes = []
    move_combos = list(product(*all_moves_list))
    for combo in move_combos:
        board = make_board(combo, node.board)
        adjacent_nodes.append(Node(board))
    return adjacent_nodes

def make_board(positions, old_board):
    new_board = {}
    for old_position, new_position in positions:
        new_board[new_position] = old_board[old_position]

        if old_board[new_position].islower():
            del old_board[new_position]
        del old_board[old_position]

    return new_board.update(old_board)

def swing_moves(position, slide_moves):
    swing_moves = []
    for move_list in slide_moves.values():
        if position in move_list:
            swing_moves += move_list.remove(position)
    return swing_moves

def slide_moves(position, board):
    r,q = position
    ran = range(-4,5)
    return [(r+i, q+j) for i in [-1,0,1] for j in [-1,0,1]
            if i != j and -(r+i)-(q+j) in ran and board[(r+i, q+j)] != "B"]
