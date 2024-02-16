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
