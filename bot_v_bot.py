from kingdomAI import agent
from kingdomAI import kingdom_board
from kingdomAI import kingdom_types
from kingdomAI.utils import print_move, print_board, print_result
from collections import deque
import time, math

TEST_MODE = False
test_move_list = deque()

def get_kingdom_move_point(row, col):
    return

def set_move_list():
    test_move_list.append(kingdom_board.Move.play(kingdom_types.Point(row=5, col=4)))  # B
    test_move_list.append(kingdom_board.Move.play(kingdom_types.Point(row=6, col=4)))  # W
    test_move_list.append(kingdom_board.Move.play(kingdom_types.Point(row=6, col=5)))  # B
    test_move_list.append(kingdom_board.Move.play(kingdom_types.Point(row=5, col=3)))  # W
    test_move_list.append(kingdom_board.Move.play(kingdom_types.Point(row=4, col=5)))  # B
    test_move_list.append(kingdom_board.Move.play(kingdom_types.Point(row=4, col=4)))  # W
    test_move_list.append(kingdom_board.Move.play(kingdom_types.Point(row=1, col=1)))  # B

def main():
    timeInterval = 0.1
    board_size = 9
    # 좌표의 시작 지점은 0 이 아닌 1 부터
    neutral_row = math.floor(board_size / 2) + 1
    neutral_col = math.floor(board_size / 2) + 1
    game = kingdom_board.GameState.new_game(board_size, neutral_row, neutral_col)
    bots = {
        kingdom_types.Player.black: agent.naive.RandomBot(),
        # kingdom_types.Player.white: agent.naive.RandomBot()
        # kingdom_types.Player.black: agent.mcts.MCTSAgent(3, 1.5)
        # kingdom_types.Player.white: agent.minimax.MinimaxAgent(3)
        kingdom_types.Player.white: agent.naive.HeuristicsBot()
    }
    print(chr(27) + "[2J")
    print_board(game)
    while not game.is_over():
        time.sleep(timeInterval)

        bot_move = bots[game.next_player].select_move(game)
        if TEST_MODE:
            if test_move_list:
                bot_move = test_move_list.popleft()
        print_move(game.next_player, bot_move)
        game = game.apply_move(bot_move)
        print(chr(27) + "[2J")
        print_board(game)

    print_result(game)

if __name__ == '__main__':
    if TEST_MODE:
        set_move_list()
    main()