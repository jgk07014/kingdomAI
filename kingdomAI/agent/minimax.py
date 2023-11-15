import enum, random
from kingdomAI.agent.base import Agent
from kingdomAI.kingdom_types import Player


MAX_SCORE = 999999
MIN_SCORE = -999999

class GameResult(enum.Enum):
    loss = 1
    draw = 2
    win = 3
def best_result_for_brute_force(game_state, max_depth):
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
        opponent_best_result = best_result_for_brute_force(next_state, max_depth - 1)
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

def alpha_beta_result(game_state, max_depth, best_black, best_white, eval_fn):
    # 게임이 종료됐는지 확인
    if game_state.is_over():
        if game_state.winner() == game_state.next_player:
            return MAX_SCORE
        else:
            return MIN_SCORE

    # 이미 최대 탐색 깊이에 도달했다. 이 흐름이 얼마나 좋았는지 가치평가함수(eval_fn)로 평가한다.
    if max_depth == 0:
        return eval_fn(game_state)

    best_so_far = MIN_SCORE
    for candidate_move in game_state.legal_moves():
        # 현재 위치에서 상대방이 낼 수 있는 최상의 결과가 무엇인지 brute force 를 수행한다.
        next_state = game_state.apply_move(candidate_move)
        opponent_best_result = alpha_beta_result(
            next_state, max_depth - 1,
            best_black, best_white,
            eval_fn)
        # 상대방이 최상의 수를 둔다고 가정하면 우리는 그 반대를 원할 것이다.
        our_result = -1 * opponent_best_result

        # 앞에서 본 최상의 결과보다 이 결과가 더 나은지 확인하자
        if our_result > best_so_far:
            best_so_far = our_result

        # 백에 대한 결과를 갱신
        if game_state.next_player == Player.white:
            if best_so_far > best_white:
                best_white = best_so_far
            # 흑이 둘 수를 선택했다. 이 수는 백의 이전 수를 들어낼 정도만 되면 된다.(?)
            outcome_for_black = -1 * best_so_far
            if outcome_for_black < best_black:
                return best_so_far
        # 흑에 대한 결과를 갱신
        elif game_state.next_player == Player.black:
            if best_so_far > best_black:
                best_black = best_so_far
            # 백이 둘 수를 선택했다. 이 수는 흑의 이전 수를 들어낼 정도만 되면 된다.(?)
            outcome_for_white = -1 * best_so_far
            if outcome_for_white < best_white:
                return best_so_far


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
            opponent_best_outcome = best_result_for_brute_force(next_state, self.max_depth)
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