def check_card_swap(x_position, y_position, joker_x, joker_y):
    # Check if the position is valid and within the bounds of the game board
    if (x_position == 1 and y_position == 7) or (x_position == 7 and y_position == 1) \
            or (x_position < 1 or x_position > 7) or (y_position < 1 or y_position > 7):
        # Invalid swap, return False
        return False

        # Check if the position coincides with the joker's position
    elif x_position == joker_x or y_position == joker_y:
        # Valid swap, return True
        return True
    else:
        # Invalid swap, return False
        return False


def store_swap(swap_x, swap_y):
    return swap_x, swap_y


def get_swap_x(swap_tuple):
    return swap_tuple[0]


def get_swap_y(swap_tuple):
    return swap_tuple[1]
