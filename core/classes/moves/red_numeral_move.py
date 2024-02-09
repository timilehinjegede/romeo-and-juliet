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
