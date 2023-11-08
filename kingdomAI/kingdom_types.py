#보드게임 관련 데이터 설정
import enum
from collections import namedtuple

class Player(enum.Enum):
    empty = 0  # 공백
    black = 1  # 선수
    white = 2  # 후수
    black_eye = 3  # 선수의 집
    white_eye = 4  # 후수의 집
    neutral = 5  # 중립

    @classmethod
    def get_eye_color(self, player):
        if player == self.black:
            return self.black_eye
        elif player == self.white:
            return self.white_eye

    def is_eye(self, value):
        return Player.black_eye == value or Player.white_eye == value

    @property
    def other(self):
        if Player.black == self:
            return Player.white
        elif Player.white == self:
            return Player.black


class Point(namedtuple('Point', 'row col')):
    #이웃한 좌표 반환
    def neighbors(self):
        return [
            Point(self.row - 1, self.col),
            Point(self.row + 1, self.col),
            Point(self.row, self.col - 1),
            Point(self.row, self.col + 1)
        ]