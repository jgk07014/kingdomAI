from kingdomAI.kingdom_types import Player
from collections import deque

def is_point_an_eye(board, point, color):
    assert board.is_on_grid(point)
    assert board._grid.get(point) is None
    if board.get_point_an_eye(point) is not None:# 한 번 집인 지점은 영원한 집이다.
        return True
    if board.get(point) is not None:# 집은 빈 점이다.
        return False
    is_exist_opposite_color = False
    is_top_edge = False
    is_bottom_edge = False
    is_left_edge = False
    is_right_edge = False

    visited = set()  # 이미 방문한 노드를 저장하기 위한 집합
    queue = deque()  # BFS를 위한 큐
    visited.add(point)
    queue.append(point)

    while queue:
        curr_point = queue.popleft()
        # 현재 노드의 인접한 방문가능한 빈 노드들을 큐에 추가하고 방문 처리
        # 단, 중립성이 아닌 상대편 돌을 마주하는 순간 bfs 중지
        for neighbor in curr_point.neighbors():
            is_top_edge = is_top_edge or neighbor.row < 1
            is_bottom_edge = is_bottom_edge or neighbor.row > board.num_rows
            is_left_edge = is_left_edge or neighbor.col < 1
            is_right_edge = is_right_edge or neighbor.col > board.num_cols
            if board.get(neighbor) is not None and ( board.get(neighbor) != color and board.get(neighbor) != Player.neutral ):
                is_exist_opposite_color = True
            if neighbor not in visited and board.get(neighbor) is None and board.is_on_grid(neighbor) and is_exist_opposite_color == False:
                visited.add(neighbor)
                queue.append(neighbor)

    touched_edge_count = is_top_edge + is_bottom_edge + is_left_edge + is_right_edge
    # 킹덤에서의 집의 정의 : 네 모서리 중에서 최대 세 모서리 이하 만큼 활용하여 자신의 돌로 둘러싸인 영역이면서, 그 영역에 상대편 돌이 존재하지 않을 경우 해당 영역을 자신의 집이라 한다.
    return touched_edge_count < 4 and is_exist_opposite_color == False