from core.classes.moves import moves


class Swap:
    def __init__(self):
        self.swapX = 0
        self.swapY = 0

    @staticmethod
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

    @staticmethod
    def suggest_swap_moves(joker_x, joker_y, player, opponent, last_x_swap, last_y_swap, board):
        """
        Suggest all valid swap moves for a player.

        :param joker_x: x position of the Joker card
        :param joker_y: y position of the Joker card
        :param player: The player object
        :param opponent: The opponent player object
        :param last_x_swap: x position of the last swapped card
        :param last_y_swap: y position of the last swapped card
        :return: List of tuples representing valid swap move coordinates
        """
        potential_swaps = []

        for x in range(1, 8):
            for y in range(1, 8):
                # Check various conditions for a valid swap
                if not (x == opponent.xPosition and y == opponent.yPosition) \
                        and not (x == player.xPosition and y == player.yPosition) \
                        and not (x == last_x_swap and y == last_y_swap) \
                        and "JOKER" not in board.get_card_string(x, y) \
                        and Swap.check_card_swap(x, y, joker_x, joker_y) \
                        and moves.check_move(x, y, opponent.xPosition, opponent.yPosition, player.player_number):
                    potential_swaps.append((x, y))

        return potential_swaps

    def store_swap(self, swap_x, swap_y):
        self.swapX = swap_x
        self.swapY = swap_y

    def get_swap_x(self):
        return self.swapX

    def get_swap_y(self):
        return self.swapY
