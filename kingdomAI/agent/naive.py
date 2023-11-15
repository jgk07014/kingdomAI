import random
from kingdomAI.agent.base import Agent
from kingdomAI.agent.helpers import is_point_an_eye
# from kingdomAI.kingdom_board import Move # (circular import bug code)
from kingdomAI.kingdom_types import Point

class RandomBot(Agent):
    def select_move(self, game_state):
        # 순환 참조 버그(circular import bug)를 방지하기 위해 Lazy Import 기법 사용
        from kingdomAI.kingdom_board import Move

        # 착수 가능한 임의의 유효한 수를 선택, 없을 경우 패스
        candidates = []
        for r in range(1, game_state.board.num_rows + 1):
            for c in range(1, game_state.board.num_cols + 1):
                candidate = Point(row=r, col=c)
                if game_state.is_valid_move(Move.play(candidate)) and \
                        not is_point_an_eye(game_state.board,
                                        candidate,
                                        game_state.next_player):
                    candidates.append(candidate)
        if not candidates:
            return Move.pass_turn()
        return Move.play(random.choice(candidates))

# 완전한 무작위 봇이 아닌 직관적 명제를 추가하여 수를 선택하는 봇
# 직관적 명제 1 : 초반 10 수 미만은 꼭짓점에 두지 않음(적용완료)
# 직관적 명제 2 : 두었을 때 자신의 활로가 늘어나는 수를 (3배 * 늘어난 활로의 수)만큼의 가중치를 추가로 부여함(미적용)
# 직관적 명제 3 : 기권은 절대 안함(적용완료)
# 직관적 명제 4 : 착수할 지점이 없을 경우에만 패스를 함(적용완료)
# 직관적 명제 5 : 초반 5 수 미만은 모서리에 두지 않음(적용완료)
# 직관적 명제 6 : 두었을 때 즉시 승리하는 수는 바로 선택함(적용완료)
# 직관적 명제 7 : 두었을 때 활로가 1 이 되는 수는 선택하지 않음(적용완료)
# 직관적 명제 8 : 두었을 때 집이 증가하는 수는 (5배 * 늘어난 집 수)만큼의 가중치를 추가로 부여함(미적용)
# 직관적 명제 9 : 두었을 때 상대방의 활로가 줄어드는 수를 (2배 * 줄어든 활로의 수)만큼의 가중치를 추가로 부여함(미적용)
class HeuristicsBot(Agent):
    initial_su1 = 10  # 초반 10 수
    initial_su2 = 5  # 초반 5 수
    weight_oppo_liberties_multiple = 2  # 2배 추가 적용
    weight_our_liberties_multiple = 3  # 3배 추가 적용
    weight_house_multiple = 5  # 5배 추가 적용

    def select_move(self, game_state):
        # 순환 참조 버그(circular import bug)를 방지하기 위해 Lazy Import 기법 사용
        from kingdomAI.kingdom_board import Move

        # 착수 가능한 임의의 유효한 수를 선택, 없을 경우 패스
        candidates = []
        candidates_weight = []
        for r in range(1, game_state.board.num_rows + 1):
            for c in range(1, game_state.board.num_cols + 1):
                weight = 1
                is_continue = False

                num_stones = len( game_state.board._grid )
                s_point = 1
                e_point = game_state.board.num_rows
                # 직관적 명제 1 : 초반 10 수 미만은 꼭짓점에 두지 않음
                if num_stones <= self.initial_su1:
                    not_moves = [
                        {"r": s_point, "c": s_point},
                        {"r": s_point, "c": e_point},
                        {"r": e_point, "c": s_point},
                        {"r": e_point, "c": e_point}
                    ] # 꼭짓점 좌표
                    # not_moves 에 해당하는 좌표일 경우 continue
                    for move in not_moves:
                        if r == move["r"] and c == move["c"]:
                            is_continue = True
                # 직관적 명제 5 : 초반 5 수 미만은 모서리에 두지 않음
                if num_stones <= self.initial_su2:
                    if r == s_point or r == e_point or c == s_point or c == e_point:
                        is_continue = True

                if is_continue:
                    continue

                candidate = Point(row=r, col=c)
                if game_state.is_valid_move(Move.play(candidate)) and \
                    not is_point_an_eye(game_state.board,
                                        candidate,
                                        game_state.next_player):
                    simulation_move = Move.play(candidate)
                    next_state = game_state.apply_move(simulation_move)
                    # 직관적 명제 7 : 두었을 때 활로가 1 이 되는 수는 선택하지 않음
                    dangerous_case = next_state.board.get_kingdom_string(candidate).num_liberties == 1
                    if dangerous_case:
                        continue
                    # 직관적 명제 6 : 두었을 때 즉시 승리하는 수는 바로 선택함
                    if next_state.is_over():
                       return Move.play(candidate)
                    # 일반적인 수는 가중치계산해서 선택할 후보 지점으로서 추가
                    candidates.append(candidate)
                    candidates_weight.append(weight)

        # 직관적 명제 3 : 기권은 절대 안함
        # 직관적 명제 4 : 착수할 지점이 없을 경우에만 패스를 함
        if not candidates:
            return Move.pass_turn()
        return Move.play(random.choice(candidates))