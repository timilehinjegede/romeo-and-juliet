from core.classes.moves import moves
from core.enums.direction import Direction


def red_numeral_move(x_position, move_count, direction):
    print("Validation for red numeral move here!")


def get_x_position_count(x_position, move_count, direction):
    # If the direction is down, add the move count to the current position
    if direction == Direction.DOWN:
        position = x_position + move_count
        # Loop to handle wrap-around if the position exceeds the upper boundary (7)
        while position > 7:
            position -= 7
        return position

    # If the direction is up, subtract the move count from the current position
    elif direction == Direction.UP:
        position = x_position - move_count
        # Loop to handle wrap-around if the position falls below the lower boundary (1)
        while position < 1:
            position += 7
        return position

    # Return 0 for invalid direction input
    else:
        return 0


def suggest_red_numeral_moves(player, move_count, opponent):
    """
    Suggest all valid moves for a player on a red numeral card.
    """
    potential_moves = []
    # Check potential moves in both directions
    for direction in [Direction.UP, Direction.DOWN]:
        x = get_x_position_count(player.xPosition, move_count, direction)
        # print("x is ({},{})".format(x, player.yPosition))

        # Check if the move is valid
        if moves.check_move(x, player.yPosition, opponent.xPosition, opponent.yPosition, player.player_number):
            potential_moves.append((x, player.yPosition))

    return potential_moves
