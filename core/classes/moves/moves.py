from core.classes.moves.black_numeral_move import black_numeral_move, get_y_position_count
from core.classes.moves.red_numeral_move import red_numeral_move, get_x_position_count
from core.classes.moves.joker_move import joker_move
from core.classes.moves.king_move import king_move
from core.classes.moves.knight_move import knight_move
from core.classes.moves.swap import Swap


def check_knight_move(x, y, new_x, new_y):
    return knight_move(x, y, new_x, new_y)


def check_joker_move(x, y, new_x, new_y):
    return joker_move(x, y, new_x, new_y)


def check_king_move(x, y, new_x, new_y):
    return king_move(x, y, new_x, new_y)


def check_black_numeral_move(x, y, new_x, new_y):
    black_numeral_move(x, y, new_x, new_y)
    return True


def check_red_numeral_move(x, y, new_x, new_y):
    red_numeral_move(x, y, new_x, new_y)
    return True


def check_swap(x, y, joker_x, joker_y):
    return Swap().check_card_swap(x, y, joker_x, joker_y)


def check_initial_move(x, y, new_x, new_y):
    return True


def check_move(x, y, opponent_player_x, opponent_player_y, player_number):
    # Check if the player's move coincides with the opponent player's position
    if x == opponent_player_x and y == opponent_player_y:
        # Invalid move, return False
        return False
    elif player_number == 1:
        # Check if the move is within bounds for player 1
        return x != 1 or y != 7
    elif player_number == 2:
        # Check if the move is within bounds for player 2
        return x != 7 or y != 1
    else:
        # Move is valid for other player numbers
        return True


def check_winning_move(x_position, y_position):
    # Check if the move results in a winning condition
    if (x_position == 7 and y_position == 1) or (x_position == 1 and y_position == 7):
        # Winning condition met
        return True
    else:
        # Winning condition not met
        return False


def y_position_count(y_position, move_count, direction):
    return get_y_position_count(y_position, move_count, direction)


def x_position_count(x_position, move_count, direction):
    return get_x_position_count(x_position, move_count, direction)


def save_swap(swap_x, swap_y):
    return Swap().store_swap(swap_x, swap_y)


def last_x_swap():
    return Swap().get_swap_x()


def last_y_swap():
    return Swap().get_swap_y()
