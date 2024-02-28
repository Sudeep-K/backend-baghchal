from django.http import JsonResponse, HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

from .utils.baghchal import Board
from .utils.mcts import *


def home_page(request):
    data = {"name": "John Doe", "age": 30, "email": "john.doe@example.com"}
    return JsonResponse(data, status=200)


@csrf_exempt
def get_best_move(request):
    board = Board()

    # initialize the board with the given state
    request_body = json.loads(request.body)
    board.position = request_body["position"]
    board.player_turn = request_body["player_turn"]
    board.goats["onHand"] = request_body["goats_onhand"]
    board.goats["killed"] = request_body["goats_killed"]
    board.tigers["trapped"] = request_body["tigers_trapped"]

    # get the best move using MCTS
    mcts = MCTS()
    best_move = mcts.search(board)
    ai_moved_board = best_move.board

    response_board_status = {
        "position": ai_moved_board.position,
        "player_turn": ai_moved_board.player_turn,
        "goats_onhand": ai_moved_board.goats["onHand"],
        "goats_killed": ai_moved_board.goats["killed"],
        "tigers_trapped": ai_moved_board.tigers["trapped"]
    }

    return JsonResponse(response_board_status, status=200, safe=False)
