def joker_move(x_position, y_position, new_x_position, new_y_position):
    # Check if the move is to the same position
    is_same_position = new_x_position == x_position and new_y_position == y_position
    # Check for specific restricted positions
    is_restricted_position = (new_x_position, new_y_position) in [(7, 1), (1, 7)]
    # Check if the position is within the board boundaries
    is_within_bounds = 1 <= new_x_position <= 7 and 1 <= new_y_position <= 7

    return not (is_same_position or is_restricted_position) and is_within_bounds


def suggest_joker_positions(board, player1, player2):
    """
    Generate a list of suggested Joker positions, excluding those occupied by players.

    :param board: The game board
    :param player1: Player 1 object
    :param player2: Player 2 object
    :return: List of tuples representing suggested Joker positions
    """
    suggested_jokers = []

    for x in range(1, 8):
        for y in range(1, 8):
            # Check if the position is marked as "JOKER" and not occupied by either player
            if "JOKER" in board.get_card_string(x, y) and not (x, y) == (player1.xPosition, player1.yPosition) \
                    and not (x, y) == (player2.xPosition, player2.yPosition):
                suggested_jokers.append((x, y))

    return suggested_jokers
