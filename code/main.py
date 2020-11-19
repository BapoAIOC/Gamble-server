from quart import Quart, request

import utils
import slots
import coinflip
import dice
import numbers

app = Quart(__name__)


@app.before_request
async def before_request():
    url_rule = request.url
    ip = request.remote_addr
    user_agent = request.headers.get("User-Agent") or ""
    utils.log_endpoint_access(url_rule, ip, user_agent)


@app.route("/slots")
async def on_slots():
    return {
        "payload": {
            "result": await slots.slots()
        }
    }, 200


@app.route("/coinflip")
async def on_coinflip():
    return {
        "payload": {
            "result": await coinflip.coinflip()
        }
    }, 200


@app.route("/dice/<int:player_count>/<int:dice_count>")
async def roll_dice(player_count: int, dice_count: int):
    return {
        "payload": {
            "result": dice.roll_n(dice_count, player_count)
        }
    }, 200


@app.route("/number/<int:count>/<int:lower>/<int:upper>")
async def get_numbers(count: int, lower: int, upper: int):
    return {
        "payload": {
            "result": [numbers.random_number_between(lower, upper) for _ in range(count)]
        }
    }


@app.route("/log/game/<int:game_id>/<float:amount>", methods=["POST"])
async def on_log(game_id: int, amount: float):
    """
    Takes:
    {
        "players": [(t_id, winner?), (t_id, winner?), (t_id, winner?)]
    }
    """
    data = await request.json
    if data is None:
        return {
            "error": "Invalid JSON"
        }, 400
    if "players" not in data:
        return utils.get_invalid_input_return("players", None)

    players = data.get("players")
    if players is None or type(players) != list:
        return utils.get_invalid_input_return("players", players)

    arg = []
    for each in players:
        if len(each) != 2:
            return utils.get_invalid_input_return("players", players)
        p, win = each
        if not isinstance(p, int) or not isinstance(win, bool):
            return utils.get_invalid_input_return("players", players)
        arg.append((p, win, ))

    return utils.log_game(game_id, amount, arg)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
