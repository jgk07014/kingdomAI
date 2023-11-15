import enum, random
from kingdomAI.agent.base import Agent


MAX_SCORE = 999999
MIN_SCORE = -999999

class GameResult(enum.Enum):
    loss = 1
    draw = 2
    win = 3
def best_result_base_is_draw(game_state, max_depth):
    if game_state.is_over():
        if game_state.winner() == game_state.next_player:
            return GameResult.win
        elif game_state.winner() is None:
            return GameResult.draw
        else:
            return GameResult.loss

    # 재귀함수 기저 조건
    if max_depth == 0:
        return GameResult.draw

    best_result_so_far = GameResult.loss
    for candidate_move in game_state.legal_moves2():
        next_state = game_state.apply_move(candidate_move)
        opponent_best_result = best_result_base_is_draw(next_state, max_depth - 1)
        our_result = reverse_game_result(opponent_best_result)
        if our_result.value > best_result_so_far.value:
            best_result_so_far = our_result
    return best_result_so_far

def best_result(game_state, max_depth, eval_fn):
    if game_state.is_over():
        if game_state.winner() == game_state.next_player:
            return MAX_SCORE
        else:
            return MIN_SCORE

    if max_depth == 0:
        # 이미 최대 탐색 깊이에 도달했다. 이 흐름이 얼마나 좋았는지 그간의 경험에 비추어 가치평가를 한다.
        return eval_fn(game_state)

    best_so_far = MIN_SCORE
    for candidate_move in game_state.legal_moves():
        # 현재 위치에서 상대방이 낼 수 있는 최상의 결과가 무엇인지 brute force 를 수행한다.
        next_state = game_state.apply_move(candidate_move)
        opponent_best_result = best_result(
            next_state, max_depth - 1, eval_fn)
        # 상대방이 최상의 수를 둔다고 가정하면 우리는 그 반대를 원할 것이다.
        our_result = -1 * opponent_best_result
        if our_result > best_so_far:
            best_so_far = our_result

def reverse_game_result(game_result):
    if game_result == GameResult.loss:
        return game_result.win
    if game_result == GameResult.win:
        return game_result.loss
    return GameResult.draw
class MinimaxAgent(Agent):
    def __init__(self, max_depth):
        self.max_depth = max_depth

    def select_move(self, game_state):
        winning_moves = []
        draw_moves = []
        losing_moves = []
        for possible_move in game_state.legal_moves2():
            #이 수를 골랐을 때 전체 게임이 어떻게 될지 계산한다.
            next_state = game_state.apply_move(possible_move)
            #상대가 다음 수를 두었을 때 거기서 나올 수 있는 최상의 결과가 무엇인지 구한다.
            opponent_best_outcome = best_result_base_is_draw(next_state, self.max_depth)
            our_best_outcome = reverse_game_result(opponent_best_outcome)
            if our_best_outcome == GameResult.win:
                winning_moves.append(possible_move)
            elif our_best_outcome == GameResult.draw:
                draw_moves.append(possible_move)
            else:
                losing_moves.append(possible_move)
        if winning_moves:
            return random.choice(winning_moves)
        if draw_moves:
            return random.choice(draw_moves)
        return random.choice(losing_moves)