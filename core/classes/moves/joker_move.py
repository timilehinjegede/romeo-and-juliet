def joker_move(x_position, y_position, new_x_position, new_y_position):
    # Check if the move is to the same position
    is_same_position = new_x_position == x_position and new_y_position == y_position
    # Check for specific restricted positions
    is_restricted_position = (new_x_position, new_y_position) in [(7, 1), (1, 7)]
    # Check if the position is within the board boundaries
    is_within_bounds = 1 <= new_x_position <= 7 and 1 <= new_y_position <= 7

    return not (is_same_position or is_restricted_position) and is_within_bounds
