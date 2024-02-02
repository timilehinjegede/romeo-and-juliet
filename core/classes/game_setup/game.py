from core.classes.game_setup.player import Player


class Game:
    def __init__(self):
        # self.players = [Player("Player 1"), Player("Player 2")]
        self.create_deck()
        self.current_turn = 0

    def create_deck(self):
        # Create and return a deck of cards
        pass

    def shuffle_deck(self):
        # Shuffle the deck
        pass

    def deal_cards(self):
        # Deal cards to players
        pass

    def check_move(self, player, card):
        # Validate player's move
        pass

    # Add other game-specific methods.
