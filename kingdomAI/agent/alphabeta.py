import enum, random
from kingdomAI.agent.base import Agent
from kingdomAI.kingdom_types import Player
from kingdomAI import kingdom_types

__all__ = [
    'AlphaBetaAgent',
]

MAX_SCORE = 999999
MIN_SCORE = -999999

def alpha_beta_result_base_is_exception(game_state, max_depth, best_black, best_white):
    # 게임이 종료됐는지 확인
    if game_state.is_over():
        if game_state.winner() == game_state.next_player:
            return MAX_SCORE
        else:
            return MIN_SCORE

    # 이미 최대 탐색 깊이에 도달했다. 아직도 결판이 나지 않았을 경우 가치 판단
    if max_depth == 0:
        return custom_eval_fn(game_state)

    best_so_far = MIN_SCORE
    for candidate_move in game_state.legal_moves2():
        # 현재 위치에서 상대방이 낼 수 있는 최상의 결과가 무엇인지 brute force 를 수행한다.
        next_state = game_state.apply_move(candidate_move)
        opponent_best_result = alpha_beta_result_base_is_exception(
            next_state, max_depth - 1,
            best_black, best_white,
            )
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
    return best_so_far

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
    for candidate_move in game_state.legal_moves2():
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
            # 흑이 둘 수를 선택했다. 이 수는 백의 이전 수를 들어낼 정도만 되면 된다.
            outcome_for_black = -1 * best_so_far
            if outcome_for_black < best_black:
                return best_so_far
        # 흑에 대한 결과를 갱신
        elif game_state.next_player == Player.black:
            if best_so_far > best_black:
                best_black = best_so_far
            # 백이 둘 수를 선택했다. 이 수는 흑의 이전 수를 들어낼 정도만 되면 된다.
            outcome_for_white = -1 * best_so_far
            if outcome_for_white < best_white:
                return best_so_far

    return best_so_far

class AlphaBetaAgent(Agent):
    def __init__(self, max_depth):
        self.max_depth = max_depth

    def select_move(self, game_state):
        best_moves = []
        best_score = None
        best_black = MIN_SCORE
        best_white = MIN_SCORE
        for possible_move in game_state.legal_moves2():
            #이 수를 골랐을 때 전체 게임이 어떻게 될지 계산한다.
            next_state = game_state.apply_move(possible_move)
            #상대가 다음 수를 두었을 때 거기서 나올 수 있는 최상의 결과가 무엇인지 구한다.
            opponent_best_outcome = alpha_beta_result_base_is_exception(
                next_state, self.max_depth,
                best_black, best_white
            )
            our_best_outcome = -1 * opponent_best_outcome
            if (not best_moves) or our_best_outcome > best_score:
                best_moves = [possible_move]
                best_score = our_best_outcome
                if game_state.next_player == Player.black:
                    best_black = best_score
                elif game_state.next_player == Player.white:
                    best_white = best_score
            elif our_best_outcome == best_score:
                best_moves.append(possible_move)
        return random.choice(best_moves)

# 직관적 명제 1 : 나의 집 개수만큼 가치 가중치 추가
def custom_eval_fn(game_state):
    black_stones = 0
    white_stones = 0
    black_eyes = 0
    white_eyes = 0
    for r in range(1, game_state.board.num_rows + 1):
        for c in range(1, game_state.board.num_cols + 1):
            p = kingdom_types.Point(r, c)
            color = game_state.board.get(p)
            if color == kingdom_types.Player.black:
                black_stones += 1
            elif color == kingdom_types.Player.white:
                white_stones += 1
            elif color == kingdom_types.Player.black_eye:
                black_eyes += 1
            elif color == kingdom_types.Player.white_eye:
                white_eyes += 1

    diff = black_eyes - white_eyes                          # <1>
    if game_state.next_player == kingdom_types.Player.black:# <2>
        return black_eyes                                   # <2>
    return white_eyes