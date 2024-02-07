from core.classes.moves.black_numeral_move import black_numeral_move
from core.classes.moves.red_numeral_move import red_numeral_move
from core.classes.moves.joker_move import joker_move
from core.classes.moves.king_move import king_move
from core.classes.moves.knight_move import knight_move
from core.classes.moves.swap import perform_swap


def check_knight_move(x, y):
    knight_move()
    return True


def check_joker_move(x, y):
    joker_move()
    return True


def check_king_move(x, y):
    king_move()
    return True


def check_black_numeral_move(x, y):
    black_numeral_move()
    return True


def check_red_numeral_move(x, y):
    red_numeral_move()
    return True


def check_swap(x, y):
    perform_swap()
    return True


def check_initial_move(x, y):
    return True

