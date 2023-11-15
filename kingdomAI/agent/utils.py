import copy
from kingdomAI.kingdom_types import Player


# 바로 이길 수를 찾는 함수
def find_winning_move(game_state, next_player):
    # 모든 가능한 수에 대해 반복한다.
    for candidate_move in game_state.legal_moves(next_player):
        # 이 수를 선택한 경우 어떤 일이 일어날지 계산한다.
        next_state = game_state.apply_move(candidate_move)
        if next_state.is_over() and next_state.is_instant_win:
            # 이 수를 두면 즉시 승리한다.
            return candidate_move
    # 이 차례에서는 이길 수 없다.
    return None