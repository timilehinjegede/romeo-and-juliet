from core.enums.direction import Direction


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


def joker_move_new(x_position, y_position, new_x_position, new_y_position, board):
    """
    Check if the Joker move is valid.

    :param x_position: Current x position of the Joker
    :param y_position: Current y position of the Joker
    :param new_x_position: New x position to move to
    :param new_y_position: New y position to move to
    :param board: The game board
    :return: True if the move is valid, False otherwise
    """
    # Check if the move is to the same position or to a restricted position
    if (new_x_position == x_position and new_y_position == y_position) \
            or (new_x_position, new_y_position) in [(7, 1), (1, 7)]:
        return False

    # Check if the position is within the board boundaries
    if not (1 <= new_x_position <= 7 and 1 <= new_y_position <= 7):
        return False

    # Check if the new position is one from which the Joker could have been reached
    card_face = board.get_card_string(new_x_position, new_y_position)
    return can_reach_joker_from(card_face, new_x_position, new_y_position, x_position, y_position)


def can_reach_joker_from(card_face, from_x, from_y, to_x, to_y):
    """
    Check if the Joker can be reached from the given position based on the card's move rules.

    :param card_face: Face of the card at the position
    :param from_x: x position of the card
    :param from_y: y position of the card
    :param to_x: x position of the Joker
    :param to_y: y position of the Joker
    :return: True if the Joker can be reached, False otherwise
    """
    # Implement logic based on the card face to determine if the Joker can be reached
    # For example, if card_face indicates a Knight, use the knight_move logic
    # You'll need to implement this logic based on your game's rules
    pass


def get_possible_moves_to_joker(joker_x, joker_y, board):
    """
    Get a list of possible moves that could have reached the Joker.

    :param joker_x: x position of the Joker
    :param joker_y: y position of the Joker
    :param board: the board
    :return: List of tuples representing possible origin coordinates
    """
    possible_origins = []
    # King can move one step in any direction
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            # Exclude the Joker's own position
            if dx == 0 and dy == 0:
                continue

            origin_x, origin_y = joker_x + dx, joker_y + dy
            # Check if the position is within the board bounds
            if 1 <= origin_x <= 7 and 1 <= origin_y <= 7:
                card_face = board.get_card_string(origin_x, origin_y)
                # If there's a King card in this position
                if 'K' in card_face and 'JOKER' not in card_face:
                    possible_origins.append((origin_x, origin_y))

    knight_moves = [(1, -2), (1, 2), (2, -1), (2, 1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    #
    # # Check each possible Knight move relative to the Joker's position
    for move in knight_moves:
        origin_x, origin_y = joker_x + move[0], joker_y + move[1]
        # Check if the position is within the board bounds
        if 1 <= origin_x <= 7 and 1 <= origin_y <= 7:
            card_face = board.get_card_string(origin_x, origin_y)
            # If there's a Knight card in this position
            if 'J' in card_face and 'JOKER' not in card_face:
                possible_origins.append((origin_x, origin_y))

    # Iterate through each position in the same row
    for y in range(1, 8):
        if y == joker_y:  # Exclude the Joker's own position
            continue

        # Get the card face and extract the move count
        card_face = board.get_card_string(joker_x, y)
        if any(char.isdigit() for char in card_face):  # Check if the card has a number
            move_count = int(''.join(filter(str.isdigit, card_face)))

            # Calculate the distance to the Joker's position
            distance = abs(joker_y - y)

            # Check if the distance matches the number on the card
            if distance == move_count:
                possible_origins.append((joker_x, y))

    # Iterate through each position in the same column
    for x in range(1, 8):
        if x != joker_x:  # Exclude the Joker's own position
            # Get the card face and extract the move count
            card_face = board.get_card_string(x, joker_y)
            if any(char.isdigit() for char in card_face):  # Check if the card has a number
                move_count = int(''.join(filter(str.isdigit, card_face)))

                # Calculate the distance to the Joker's position
                distance = abs(joker_x - x)

                # Check if the distance matches the number on the card
                if distance == move_count:
                    possible_origins.append((x, joker_y))

    return possible_origins


def calculate_chebyshev_distance(point_a, point_b):
    return max(abs(point_a[0] - point_b[0]), abs(point_a[1] - point_b[1]))


def evaluate_joker_move(origin, current_position, opponent_position, strategic_positions):
    # Example evaluation criteria
    score = 0

    # Proximity to objectives
    for objective in strategic_positions:
        score -= calculate_chebyshev_distance(origin, objective)

    # Safety from opponents
    score -= calculate_chebyshev_distance(origin, opponent_position) * 2  # Weighted for demonstration

    return score


def best_joker_move(joker_x, joker_y, board, opponent_position, strategic_positions):
    potential_origins = get_possible_moves_to_joker(joker_x, joker_y, board)
    best_move = None
    best_score = float('-inf')

    for origin in potential_origins:
        score = evaluate_joker_move(origin, (joker_x, joker_y), opponent_position, strategic_positions)
        if score > best_score:
            best_score = score
            best_move = origin

    return best_move
