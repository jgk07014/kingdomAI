from kingdomAI import kingdom_types

COLS = 'ABCDEFGHJKLMNOPQRST'# I 는 1 과 헷갈릴 수 있으므로 빼는 것이 관례이다. 최대 19 열
STONE_TO_CHAR = {
    None: ' . ',
    kingdom_types.Player.neutral: ' ★ ',
    kingdom_types.Player.black: ' B ',
    kingdom_types.Player.white: ' W ',
    kingdom_types.Player.black_eye : ' ■ ',
    kingdom_types.Player.white_eye : ' □ '
}

def print_move(player, move):
    if move.is_pass:
        move_str = 'passes'
    elif move.is_resign:
        move_str = 'resigns'
    else:
        move_str = '%s%d' % (COLS[move.point.col - 1], move.point.row)
    print('%s %s' % (player, move_str))

def print_board(game):
    board = game.board
    for row in range(board.num_rows, 0, -1):
        bump = " " if row <= 9 else ""
        line = []
        for col in range(1, board.num_cols + 1):
            stone_or_eye = board.get(kingdom_types.Point(row=row, col=col))
            line.append(STONE_TO_CHAR[stone_or_eye])
        print('%s%d %s' % (bump, row, ''.join(line)))
    print('    ' + '  '.join(COLS[:board.num_cols]))

def print_result(game):
    board = game.board
    black_eye_count = 0
    white_eye_count = 0
    for row in range(1, board.num_rows + 1, 1):
        for col in range(1, board.num_cols + 1):
            point = kingdom_types.Point(row=row, col=col)
            if board.get_point_an_eye(point) == kingdom_types.Player.black_eye:
                black_eye_count += 1
            if board.get_point_an_eye(point) == kingdom_types.Player.white_eye:
                white_eye_count += 1
    if not game.is_instant_win:
        print("Black Eye : %d" %(black_eye_count))
        print("White Eye : %d" %(white_eye_count))
    win_msg = None
    if game.is_instant_win:
        last_player = board.get(game.last_move.point)
        if last_player == kingdom_types.Player.black:
            win_msg = ("Black Destory Win")
        elif last_player == kingdom_types.Player.white:
            win_msg = ("White Destroy Win")
    else:
        if black_eye_count > white_eye_count:
            win_msg = "Black Score Win!!"
        elif black_eye_count < white_eye_count:
            win_msg = "White Score Win!!"
        else:
            win_msg = "Draw..."
    print(win_msg)

def point_from_coords(coords):
    col = COLS.index(coords[0]) + 1
    row = int(coords[1:])
    return kingdom_types.Point(row=row, col=col)