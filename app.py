from flask import Flask, request, json, jsonify

app = Flask(__name__)

@app.route("/ai_difficulty_easy", methods=['POST'])
def ai_difficulty_easy():
    # 순환 참조 버그(circular import bug)를 방지하기 위해 Lazy Import 기법 사용
    from kingdomAI import agent, util

    params = request.get_json()
    bots = agent.naive.RandomBot()
    game = util.convertKingdomGameToJsonData(params)
    bot_move = bots.select_move(game)
    adjusted_col = None
    adjusted_row = None
    if bot_move.is_play:
        # 좌표는 0부터 n-1 이 아닌 1부터 n까지 이므로 -1 을 함.
        adjusted_col = bot_move.point.col - 1
        adjusted_row = bot_move.point.row - 1
    response = {
        "col": adjusted_col,
        "row": adjusted_row
    }
    return jsonify(response)

@app.route("/ai_difficulty_normal", methods=['POST'])
def ai_difficulty_normal():
    # 순환 참조 버그(circular import bug)를 방지하기 위해 Lazy Import 기법 사용
    from kingdomAI import agent, util

    params = request.get_json()
    bots = agent.naive.HeuristicsBot()
    game = util.convertKingdomGameToJsonData(params)
    bot_move = bots.select_move(game)
    adjusted_col = None
    adjusted_row = None
    if bot_move.is_play:
        # 좌표는 0부터 n-1 이 아닌 1부터 n까지 이므로 -1 을 함.
        adjusted_col = bot_move.point.col - 1
        adjusted_row = bot_move.point.row - 1
    response = {
        "col": adjusted_col,
        "row": adjusted_row
    }
    return jsonify(response)

@app.route("/ai_difficulty_hard", methods=['POST'])
def ai_difficulty_hard():
    # 순환 참조 버그(circular import bug)를 방지하기 위해 Lazy Import 기법 사용
    from kingdomAI import agent, util

    params = request.get_json()
    bots = agent.naive.HeuristicsBot()
    game = util.convertKingdomGameToJsonData(params)
    bot_move = bots.select_move(game)
    adjusted_col = None
    adjusted_row = None
    if bot_move.is_play:
        # 좌표는 0부터 n-1 이 아닌 1부터 n까지 이므로 -1 을 함.
        adjusted_col = bot_move.point.col - 1
        adjusted_row = bot_move.point.row - 1
    response = {
        "col": adjusted_col,
        "row": adjusted_row
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=False, host='127.0.0.1', port=8080)