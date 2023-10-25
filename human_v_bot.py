from kingdomAI import agent
from kingdomAI import kingdom_board
from kingdomAI import kingdom_types
from kingdomAI.utils import print_move, print_board, print_result, point_from_coords
from collections import deque
import time, math

TEST_MODE = False
test_move_list = deque()

def get_kingdom_move_point(row, col):
    return

def set_move_list():
    test_move_list.append(kingdom_board.Move.play(kingdom_types.Point(row=5, col=4)))  # AI
    test_move_list.append(kingdom_board.Move.play(kingdom_types.Point(row=6, col=4)))  # AI
    test_move_list.append(kingdom_board.Move.play(kingdom_types.Point(row=6, col=5)))  # AI
    test_move_list.append(kingdom_board.Move.play(kingdom_types.Point(row=5, col=3)))  # AI
    test_move_list.append(kingdom_board.Move.play(kingdom_types.Point(row=4, col=5)))  # AI
    test_move_list.append(kingdom_board.Move.play(kingdom_types.Point(row=4, col=4)))  # AI
    test_move_list.append(kingdom_board.Move.play(kingdom_types.Point(row=1, col=1)))  # AI

def main():
    timeInterval = 1
    board_size = 9
    # 좌표의 시작 지점은 0 이 아닌 1 부터
    neutral_row = math.floor(board_size / 2) + 1
    neutral_col = math.floor(board_size / 2) + 1
    game = kingdom_board.GameState.new_game(board_size, neutral_row, neutral_col)
    bots = agent.naive.RandomBot()
    print(chr(27) + "[2J")
    print_board(game)
    while not game.is_over():
        if game.next_player == kingdom_types.Player.black:
            human_move = input('-- ')
            point = point_from_coords(human_move.strip())
            move = kingdom_board.Move.play(point)
        else:
            time.sleep(timeInterval)
            bot_move = bots.select_move(game)
            if TEST_MODE:
                if test_move_list:
                    bot_move = test_move_list.popleft()
            move = bot_move
        print_move(game.next_player, move)
        game = game.apply_move(move)
        print(chr(27) + "[2J")
        print_board(game)
    print_result(game)

if __name__ == '__main__':
    if TEST_MODE:
        set_move_list()
    main()