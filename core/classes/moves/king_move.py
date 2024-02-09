def king_move(x_position, y_position, new_x_position, new_y_position):
    # Check if the move is within the board bounds
    if not (0 < new_x_position < 8 and 0 < new_y_position < 8):
        return False

    # Check if the move is either horizontal, vertical, or diagonal by one step
    x_diff = abs(new_x_position - x_position)
    y_diff = abs(new_y_position - y_position)

    # Valid move if both differences are at most 1 and not both zero (move to a different position)
    return (x_diff <= 1 and y_diff <= 1) and not (x_diff == 0 and y_diff == 0)
