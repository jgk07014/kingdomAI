from kingdomAI import kingdom_types, kingdom_board
from kingdomAI.kingdom_board import Move, KingdomString
from kingdomAI.kingdom_types import Point
from kingdomAI.utils import print_board


def convertKingdomGameToJsonData(jsonData):
    board_state = jsonData['board']
    next_player_color = jsonData['nextPlayerColor']
    board_size = jsonData['boardSize']
    neutral_row = jsonData['neutralRow']
    neutral_col = jsonData['neutralCol']
    # 좌표는 0부터 n-1 이 아닌 1부터 n까지 이므로 +1 을 함.
    adjusted_neutral_row = neutral_row + 1
    adjusted_neutral_col = neutral_col + 1
    game = kingdom_board.GameState.new_game(board_size, adjusted_neutral_row, adjusted_neutral_col)
    Player = kingdom_types.Player

    # 해당 좌표의 돌이 놓여져 있으면 (집업데이트 하지 않는 옵션으로) 강제로 해당 좌표에 착수
    for row in range(len(board_state)):
        for col in range(len(board_state[row])):
            state = board_state[row][col]
            # 좌표는 0부터 n-1 이 아닌 1부터 n까지 이므로 +1 을 함.
            adjusted_row = row + 1
            adjusted_col = col + 1
            if state == Player.black.value:
                game.next_player = Player.black
                point = Point(adjusted_row, adjusted_col)
                move = Move.play(point)
                # game = game.apply_move(move) # 2중 for 문 순서대로 착수할 경우 집의 발생 타이밍에 따라 버그 발생
                game = game.custom_apply_move(move)
            if state == Player.white.value:
                game.next_player = Player.white
                point = Point(adjusted_row, adjusted_col)
                move = Move.play(point)
                # game = game.apply_move(move) # 2중 for 문 순서대로 착수할 경우 집의 발생 타이밍에 따라 버그 발생
                game = game.custom_apply_move(move)

    # 해당 좌표의 돌이 놓여져 있으면 (집업데이트 하지 않는 옵션으로) 강제로 해당 좌표에 착수
    for row in range(len(board_state)):
        for col in range(len(board_state[row])):
            state = board_state[row][col]
            # 좌표는 0부터 n-1 이 아닌 1부터 n까지 이므로 +1 을 함.
            adjusted_row = row + 1
            adjusted_col = col + 1
            if state == Player.black_eye.value:
                game.next_player = Player.black
                point = Point(adjusted_row, adjusted_col)
                alreadyUpdated = game.board.get_point_an_eye(point) is not None
                if not alreadyUpdated:
                    game.board.update_eye(game.next_player, point)
            if state == Player.white_eye.value:
                game.next_player = Player.white
                point = Point(adjusted_row, adjusted_col)
                alreadyUpdated = game.board.get_point_an_eye(point) is not None
                if not alreadyUpdated:
                    game.board.update_eye(game.next_player, point)
    game.next_player = Player(next_player_color)
    print_board(game)

    return game
