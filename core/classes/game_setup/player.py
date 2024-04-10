class Player:
    def __init__(self, name, player_number):
        self.name = name
        self.player_number = player_number
        # Initialize an empty list for storing the player's moves
        self.moves = []
        self.currentScore = 0

        # Set initial positions based on player number
        if player_number == 1:
            # Player 1 starts at position (1, 7) on the board, which is at the top left
            self.xPosition = 7
            self.yPosition = 1
        elif player_number == 2:
            # Player 2 starts at position (7, 1) on the board, which is at the bottom right
            self.xPosition = 1
            self.yPosition = 7
        else:
            # Default position if player number is not 1 or 2
            self.xPosition = 0
            self.yPosition = 0

    # Set the player's position on the board
    def set_position(self, x, y):
        self.xPosition = x
        self.yPosition = y

    # Return the player's current x position
    def get_x_position(self):
        return self.xPosition

    # Return the player's current y position
    def get_y_position(self):
        return self.yPosition

    # Record a new move made by the player
    def record_move(self, move):
        return self.moves.append(move)

    # Return a list of all moves made by the player
    def get_moves(self):
        return self.moves
