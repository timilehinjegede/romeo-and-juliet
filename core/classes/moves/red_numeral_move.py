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


def best_red_numeral_move(player, move_count, opponent, goal_position):
    potential_moves = suggest_red_numeral_moves(player, move_count, opponent)
    best_move = None
    best_score = float('-inf')  # Initialize with the lowest possible score

    for move in potential_moves:
        score = evaluate_move(move, player, opponent, goal_position)

        if score > best_score:
            best_score = score
            best_move = move

    return best_move


def evaluate_move(move, player, opponent, goal_position):
    score = 0
    move_x, move_y = move

    # Calculate the distance to the goal and inversely adjust the score
    goal_distance = calculate_distance(move_x, move_y, goal_position.x, goal_position.y)
    score -= goal_distance  # Less distance is better

    # Add more evaluations as needed, for example, avoiding the opponent
    opponent_distance = calculate_distance(move_x, move_y, opponent.xPosition, opponent.yPosition)
    score += opponent_distance  # More distance from the opponent is better

    return score


def calculate_distance(x1, y1, x2, y2):
    # Using Manhattan distance as a simple metric for grid movement
    return abs(x1 - x2) + abs(y1 - y2)

