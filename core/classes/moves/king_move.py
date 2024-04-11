from core.classes.moves import moves


def king_move(x_position, y_position, new_x_position, new_y_position):
    # Check if the move is within the board bounds
    if not (0 < new_x_position < 8 and 0 < new_y_position < 8):
        return False

    # Check if the move is either horizontal, vertical, or diagonal by one step
    x_diff = abs(new_x_position - x_position)
    y_diff = abs(new_y_position - y_position)

    # Valid move if both differences are at most 1 and not both zero (move to a different position)
    return (x_diff <= 1 and y_diff <= 1) and not (x_diff == 0 and y_diff == 0)


def suggest_king_moves(x_position, y_position, opponent_player_x, opponent_player_y, player_number):
    """
    Suggest all valid moves for a king piece from the current position.

    :param x_position: Current x position of the king
    :param y_position: Current y position of the king
    :param opponent_player_x: Opponent's x position
    :param opponent_player_y: Opponent's y position
    :param player_number: The number of the player making the move
    :return: List of tuples representing valid move coordinates
    """
    potential_moves = []
    for x in range(x_position - 1, x_position + 2):
        for y in range(y_position - 1, y_position + 2):
            if 0 < x < 8 and 0 < y < 8 and not (x == x_position and y == y_position):
                if moves.check_move(x, y, opponent_player_x, opponent_player_y, player_number):
                    potential_moves.append((x, y))

    # Returns a list of all valid moves the king can make from its current position
    return potential_moves


def evaluate_king_move(x, y, goal_x, goal_y):
    # Simple Euclidean distance for evaluation
    return ((x - goal_x) ** 2 + (y - goal_y) ** 2) ** 0.5


def best_king_move(x_position, y_position, opponent_x, opponent_y, goal_x, goal_y, player_number):
    potential_moves = suggest_king_moves(x_position, y_position, opponent_x, opponent_y, player_number)
    best_move = None
    min_distance = float('inf')  # Start with an infinitely large distance

    for move in potential_moves:
        new_x, new_y = move
        distance = evaluate_king_move(new_x, new_y, goal_x, goal_y)

        # Update best move if this move is closer to the goal
        if distance < min_distance:
            min_distance = distance
            best_move = move

    return best_move

