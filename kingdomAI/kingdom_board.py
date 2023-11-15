import copy
from collections import deque
from kingdomAI.kingdom_types import Player, Point
from kingdomAI.agent.helpers import is_point_an_eye


class Move():
    # 기사가 자기 차례에 할 수 있는 행동(is_play, is_pass, is_resign) 세팅
    def __init__(self, point=None, is_pass=False, is_resign=False):
        assert (point is not None) ^ is_pass ^ is_resign
        self.point = point
        self.is_play = (self.point is not None)
        self.is_pass = is_pass
        self.is_resign = is_resign

    # 돌 놓기
    @classmethod
    def play(cls, point):
        return Move(point=point)

    # 차례 넘기기
    @classmethod
    def pass_turn(cls):
        return Move(is_pass=True)

    # 기권 선언
    @classmethod
    def resign(cls):
        return Move(is_resign=True)


class KingdomString():
    def __init__(self, color, stones, liberties):
        self.color = color
        self.stones = set(stones)
        self.liberties = set(liberties)

    def remove_liberty(self, point):
        self.liberties.remove(point)

    def add_liberty(self, point):
        self.liberties.add(point)

    # 인접한 이음의 모든 돌을 저장한 새 이음을 반환
    def merged_with(self, kingdom_string):
        assert kingdom_string.color == self.color
        combined_stones = self.stones | kingdom_string.stones
        return KingdomString(
            self.color,
            combined_stones,
            (self.liberties | kingdom_string.liberties) - combined_stones
        )

    @property
    def num_liberties(self):
        return len(self.liberties)

    # 파이썬의 문법 __eq__ 는 스페셜 메서드명으로 비교연산을 정의하는 부분
    def __eq__(self, other):
        return isinstance(other, KingdomString) and \
            self.color == other.color and \
            self.stones == other.stones and \
            self.liberties == other.liberties


class Board():
    def __init__(self, num_rows, num_cols, neutral_row, neutral_col):
        self.num_rows = num_rows  # 보드판의 세로 길이
        self.num_cols = num_cols  # 보드판의 가로 길이
        self._grid = {}  # 착수된 각각의 좌표에 대한 이음(string) 집합
        self._eye = {}  # 집으로 완성된 좌표에 대한 플레이어(player) 집합
        neutral_point = Point(row=neutral_row, col=neutral_col)
        self.place_stone(Player.neutral, neutral_point)# 중립성의 위치 초기 설정

    def place_stone(self, player, point):
        assert self.get_point_an_eye(point) is None
        assert self.is_on_grid(point)
        assert self._grid.get(point) is None
        is_win_game = False
        adjacent_same_color = []
        adjacent_opposite_color = []
        liberties = []
        for neighbor in point.neighbors():
            if not self.is_on_grid(neighbor):
                continue
            neighbor_string = self._grid.get(neighbor)
            if neighbor_string is None:
                liberties.append(neighbor)
            elif neighbor_string.color == player:
                if neighbor_string not in adjacent_same_color:
                    adjacent_same_color.append(neighbor_string)
            elif neighbor_string.color == player.other:
                if neighbor_string not in adjacent_opposite_color:
                    adjacent_opposite_color.append(neighbor_string)
        new_string = KingdomString(player, [point], liberties)
        # 같은 색의 근접한 이음을 합친다.
        for same_color_string in adjacent_same_color:
            new_string = new_string.merged_with(same_color_string)
        # 새롭게 돌을 착수한다.
        for new_string_point in new_string.stones:
            self._grid[new_string_point] = new_string
        # 다른 색의 근접한 이음의 활로를 줄인다.
        for other_color_string in adjacent_opposite_color:
            other_color_string.remove_liberty(point)
        # 다른 색 이음의 활로가 0이 되면 그 돌을 제거한다.
        for other_color_string in adjacent_opposite_color:
            if other_color_string.num_liberties == 0:
                is_win_game = True
                self._remove_string(other_color_string)
        # 이웃한 집이 아닌 빈 좌표를 bfs 시작지점으로 설정하여 이번 착수로 인해 신규로 생성된 집을 추가한다.
        for neighbor in point.neighbors():
            if self._grid.get(neighbor) is None and self._eye.get(neighbor) is None and self.is_on_grid(neighbor):
                self.update_eye(player, neighbor)
        # 착수해서 상대방 돌을 따내는 순간 즉시 승리
        return is_win_game

    def custom_place_stone(self, player, point):
        assert self.get_point_an_eye(point) is None
        assert self.is_on_grid(point)
        assert self._grid.get(point) is None
        is_win_game = False
        adjacent_same_color = []
        adjacent_opposite_color = []
        liberties = []
        for neighbor in point.neighbors():
            if not self.is_on_grid(neighbor):
                continue
            neighbor_string = self._grid.get(neighbor)
            if neighbor_string is None:
                liberties.append(neighbor)
            elif neighbor_string.color == player:
                if neighbor_string not in adjacent_same_color:
                    adjacent_same_color.append(neighbor_string)
            elif neighbor_string.color == player.other:
                if neighbor_string not in adjacent_opposite_color:
                    adjacent_opposite_color.append(neighbor_string)
        new_string = KingdomString(player, [point], liberties)
        # 같은 색의 근접한 이음을 합친다.
        for same_color_string in adjacent_same_color:
            new_string = new_string.merged_with(same_color_string)
        # 새롭게 돌을 착수한다.
        for new_string_point in new_string.stones:
            self._grid[new_string_point] = new_string
        # 다른 색의 근접한 이음의 활로를 줄인다.
        for other_color_string in adjacent_opposite_color:
            other_color_string.remove_liberty(point)
        # 다른 색 이음의 활로가 0이 되면 그 돌을 제거한다.
        for other_color_string in adjacent_opposite_color:
            if other_color_string.num_liberties == 0:
                is_win_game = True
                self._remove_string(other_color_string)
        # custom 에서는 집 업데이트를 하지 않는 옵션이 추가됨.(패킷받을 때 강제로 착수하는 알고리즘의 필요에 의해 만들어진 옵션)
        # # 이웃한 집이 아닌 빈 좌표를 bfs 시작지점으로 설정하여 이번 착수로 인해 신규로 생성된 집을 추가한다.
        # for neighbor in point.neighbors():
        #     if self._grid.get(neighbor) is None and self._eye.get(neighbor) is None and self.is_on_grid(neighbor):
        #         self.update_eye(player, neighbor)
        # 착수해서 상대방 돌을 따내는 순간 즉시 승리
        return is_win_game

    # 주어진 좌표로 부터 bfs 탐색을 할 때 집이될 수 있으면 집 업데이트
    def update_eye(self, player, point):
        assert self.get_point_an_eye(point) is None
        assert self.is_on_grid(point)
        assert self._grid.get(point) is None

        is_update = is_point_an_eye(self, point, player)#해당 지점이 집이면 업데이트를 해야한다.

        if is_update:
            visited = set()
            queue = deque()
            visited.add(point)
            queue.append(point)
            self._eye[point] = Player.get_eye_color(player)
            while queue:
                curr_point = queue.popleft()
                for neighbor in curr_point.neighbors():
                    if neighbor not in visited and self.is_on_grid(neighbor) and self.get(neighbor) is None:
                        visited.add(neighbor)
                        queue.append(neighbor)
                        self._eye[neighbor] = Player.get_eye_color(player)

    def _remove_string(self, string):
        for point in string.stones:
            for neighbor in point.neighbors():
                neighbor_string = self._grid.get(neighbor)
                if neighbor_string is None:
                    continue
                if neighbor_string is not string:
                    neighbor_string.add_liberty(point)
            self._grid[point] = None

    # 해당 좌표값(point)이 보드판 위에 존재할 수 있는 유효한 좌표값인지 판별하는 메서드
    def is_on_grid(self, point):
        return 1 <= point.row <= self.num_rows and \
            1 <= point.col <= self.num_cols

    # 해당 좌표값(point)이 집(eye)이면 집의 색깔, 아니면 None 을 반환하는 메서드
    def get_point_an_eye(self, point):
        eye_color = self._eye.get(point)
        if eye_color is None:
            return None
        return eye_color

    # 바둑판 위의 점 내용을 반환(만약 돌이 해당 점 위에 있으면 Player 를 반환하고, 아니면 None 을 반환한다.)
    def get(self, point):
        string = self._grid.get(point)
        if string is None:
            #돌이 놓여져 있지 않은 공간이라도 집일 수 있다.
            eye = self.get_point_an_eye(point)
            return eye#집도 아닐 경우 None 이 반환됨.
        return string.color

    # 해당 점의 돌에 연결된 모든 이음을 반환(만약 돌이 해당 점 위에 있으면 KingdomString 을 반환하고, 아니면 None 을 반환한다.)
    def get_kingdom_string(self, point):
        string = self._grid.get(point)
        if string is None:
            return None
        return string


class GameState():
    def __init__(self, board, next_player, previous, move):
        self.board = board
        self.next_player = next_player
        self.previous_state = previous
        self.last_move = move
        self.is_instant_win = False#즉시승리 여부(상대방 성 파괴)

    # 수를 둔 후 새 GameState 반환
    def apply_move(self, move):
        is_instant_win = False
        if move.is_play:
            next_board = copy.deepcopy(self.board)
            is_instant_win = next_board.place_stone(self.next_player, move.point)
        else:
            next_board = self.board
        game = GameState(next_board, self.next_player.other, self, move)
        game.is_instant_win = is_instant_win
        return game

    def custom_apply_move(self, move):
        is_instant_win = False
        if move.is_play:
            next_board = copy.deepcopy(self.board)
            is_instant_win = next_board.custom_place_stone(self.next_player, move.point)
        else:
            next_board = self.board
        game = GameState(next_board, self.next_player.other, self, move)
        game.is_instant_win = is_instant_win
        return game

    # 대국 종료 판단
    def is_over(self):
        if self.is_instant_win:
            return True
        if self.last_move is None:
            return False
        if self.last_move.is_resign:
            return True
        second_last_move = self.previous_state.last_move
        if second_last_move is None:
            return False
        return self.last_move.is_pass and second_last_move.is_pass

    # 대국 종료시 승자 판단
    def winner(self):
        result = None

        if(self.is_instant_win):
            result = self.next_player.other
        else:
            black_eye_count = self.get_player_eye_count(Player.black)
            white_eye_count = self.get_player_eye_count(Player.white)
            is_black_win = black_eye_count > white_eye_count
            is_white_win = black_eye_count < white_eye_count
            if is_black_win:
                result = Player.black
            elif is_white_win:
                result = Player.white
            else:
                result = None

        # 무승부 혹은 승패가 결정되지 않은 상태일 경우 None 상태
        return result

    # 인자로 주어진 플레이어의 현재 점수 계산
    def get_player_eye_count(self, player):
        count = 0
        for row in range(1, self.board.num_rows + 1):
            for col in range(1, self.board.num_cols + 1):
                point = Point(row, col)
                eye = self.board.get_point_an_eye(point)
                if eye == player.get_eye_color(player):
                    count = count + 1
        return count

    # 인자로 주어진 플레이어의 현재 모든 활로의 수 계산
    def get_player_all_liberties_count(self, player):
        all_num_liberties = 0
        for value in self.board._grid.values():
            if value.color == player:
                all_num_liberties += value.num_liberties
        return all_num_liberties

    # 가능한 모든 행동 리스트
    def legal_moves(self):
        moves = []
        for row in range(1, self.board.num_rows + 1):
            for col in range(1, self.board.num_cols + 1):
                move = Move.play(Point(row, col))
                if self.is_valid_move(move):
                    moves.append(move)
        # These two moves are always legal
        moves.append(Move.pass_turn())
        moves.append(Move.resign())
        return moves

    # 실력 향상을 위해서 직관적 명제 추가
    # 착수할 지점이 있으면 패스나 기권을 하지 않을 예정, 착수할 지점이 없으면 패스, 기권은 존재하지 않음.
    def legal_moves2(self):
        exist_move_point = None
        moves = []
        for row in range(1, self.board.num_rows + 1):
            for col in range(1, self.board.num_cols + 1):
                move = Move.play(Point(row, col))
                if self.is_valid_move(move):
                    exist_move_point = True
                    moves.append(move)
        # These two moves are always legal but except move_pass
        if exist_move_point:
            moves.append(Move.pass_turn())
            # moves.append(Move.resign())
        return moves

    # 자충수 여부 확인
    def is_move_self_capture(self, player, move):
        if not move.is_play:
            return False
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, move.point)
        new_string = next_board.get_kingdom_string(move.point)
        return new_string.num_liberties == 0

    @classmethod
    def new_game(cls, board_size, neutral_row, neutral_col):
        if isinstance(board_size, int):
            board_size = (board_size, board_size)
            board = Board(*board_size, neutral_row, neutral_col)
        return GameState(board, Player.black, None, None)

    @property
    def situation(self):
        return (self.next_player, self.board)

    def is_valid_move(self, move):
        if self.is_over():
            return False
        if move.is_pass or move.is_resign:
            return True
        return (
                self.board.get(move.point) is None and
                self.board.get_point_an_eye(move.point) is None and
                not self.is_move_self_capture(self.next_player, move))
