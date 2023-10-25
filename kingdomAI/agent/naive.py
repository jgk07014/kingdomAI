import random
from kingdomAI.agent.base import Agent
from kingdomAI.agent.helpers import is_point_an_eye
from kingdomAI.kingdom_board import Move
from kingdomAI.kingdom_types import Point

class RandomBot(Agent):
    def select_move(self, game_state):
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