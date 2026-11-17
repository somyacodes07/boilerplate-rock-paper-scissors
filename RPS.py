# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.

BEAT = {"R": "P", "P": "S", "S": "R"}  # move that beats the key
CYCLE = ["R", "R", "P", "P", "S"]


# Each model predicts the opponent's NEXT move, given my moves so far.
def _quincy(mine, n):
    return CYCLE[(n + 1) % 5]


def _kris(mine, n):
    return "P" if n == 0 else BEAT[mine[-1]]


def _mrugesh(mine, n):
    last_ten = ([""] + mine[:n])[-10:]
    most = max(set(last_ten), key=last_ten.count)
    return BEAT["S" if most == "" else most]


def _abbey(mine, n):
    h = ["R"] + mine[:n]
    counts = {}
    for i in range(len(h) - 1):
        pair = h[i] + h[i + 1]
        counts[pair] = counts.get(pair, 0) + 1
    options = {h[-1] + m: counts.get(h[-1] + m, 0) for m in "RPS"}
    return BEAT[max(options, key=options.get)[-1]]


MODELS = [_quincy, _kris, _mrugesh, _abbey]


def player(prev_play, opponent_history=[], state={}):
    # A new match starts with an empty string: reset everything.
    if prev_play == "":
        opponent_history.clear()
        state.clear()
        state["mine"] = []
        state["scores"] = [0.0] * len(MODELS)
        state["preds"] = [None] * len(MODELS)
    else:
        opponent_history.append(prev_play)
        # Score each model on whether it predicted the opponent's last move.
        for i, pred in enumerate(state["preds"]):
            hit = 1.0 if pred == prev_play else 0.0
            state["scores"][i] = state["scores"][i] * 0.9 + hit

    mine = state["mine"]
    n = len(mine)
    state["preds"] = [m(mine, n) for m in MODELS]

    best = max(range(len(MODELS)), key=lambda i: state["scores"][i])
    if state["scores"][best] < 3 and n > 10:
        guess = "R"  # no model fits well; fall back
    else:
        guess = state["preds"][best]

    move = BEAT[guess]
    mine.append(move)
    return move