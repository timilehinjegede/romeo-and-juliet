from core.classes.moves import moves
from core.enums.direction import Direction


def black_numeral_move(x_position, move_count, direction):
    print("Black numeral move validation here!")


def get_y_position_count(y_position, move_count, direction):
    # Calculates the new Y position based on the current position, move count, and direction
    if direction == Direction.RIGHT:
        # If moving right, add the move count to the current position
        position = y_position + move_count
        # Wrap around if the position exceeds the upper limit of 7
        while position > 7:
            position -= 7
        return position
    elif direction == Direction.LEFT:
        # If moving left, subtract the move count from the current position
        position = y_position - move_count
        # Wrap around if the position goes below the lower limit of 1
        while position < 1:
            position += 7
        return position
    else:
        # Return 0 if an invalid direction is provided
        return 0


def suggest_black_numeral_moves(player, move_count, opponent):
    """
    Suggest all valid moves for a player on a black numeral card.
    :return: List of y-positions representing valid move coordinates
    """
    potential_moves = []
    # Check potential moves in both directions
    for direction in [Direction.RIGHT, Direction.LEFT]:
        y = get_y_position_count(player.yPosition, move_count, direction)
        print("y is ({},{})".format(player.xPosition, y))
        # Check if the move is valid
        if moves.check_move(player.xPosition, y, opponent.xPosition, opponent.yPosition, player.player_number):
            potential_moves.append((player.xPosition, y))

    return potential_moves
