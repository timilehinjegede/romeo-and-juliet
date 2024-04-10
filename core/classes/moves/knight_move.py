from core.classes.moves import moves


def knight_move(x_position, y_position, new_x_position, new_y_position):
    # Check if new position is different and within board boundaries
    if (new_x_position != x_position or new_y_position != y_position) and (0 < new_x_position < 8) and (
            0 < new_y_position < 8):
        # Define possible moves for a knight (how a knight moves)
        valid_moves = [(1, -2), (1, 2), (2, -1), (2, 1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
        # Check if the move is one of the valid moves
        return (new_x_position - x_position, new_y_position - y_position) in valid_moves
    return False


def suggest_knight_moves(player, opponent):

    potential_moves = []
    knight_moves = [(1, -2), (1, 2), (2, -1), (2, 1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]

    for move in knight_moves:
        new_x, new_y = player.xPosition + move[0], player.yPosition + move[1]
        # Check if the move is different, within board boundaries, and valid
        if (new_x != player.xPosition or new_y != player.yPosition) and (0 < new_x < 8) and (0 < new_y < 8):
            if moves.check_move(new_x, new_y, opponent.xPosition, opponent.yPosition, player.player_number):
                potential_moves.append((new_x, new_y))

    return potential_moves


def evaluate_knight_move(move, player, opponent, goal_position):
    score = 0
    move_x, move_y = move

    # Proximity to Objective: Closer moves are better
    goal_distance = abs(move_x - goal_position.x) + abs(move_y - goal_position.y)
    score -= goal_distance  # Decrease score by distance to goal

    # Avoiding the Opponent: Prefer moves that increase distance from the opponent
    opponent_distance = abs(move_x - opponent.xPosition) + abs(move_y - opponent.yPosition)
    score += max(0, opponent_distance - 1)  # Only score for moves more than 1 step away from the opponent

    return score


def best_knight_move(player, opponent, goal_position):
    potential_moves = suggest_knight_moves(player, opponent)
    best_move = None
    best_score = float('-inf')

    for move in potential_moves:
        score = evaluate_knight_move(move, player, opponent, goal_position)
        if score > best_score:
            best_score = score
            best_move = move

    return best_move
