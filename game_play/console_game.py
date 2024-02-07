from core.classes.game_setup.board import Board
from core.classes.game_setup.pack import Pack
from core.classes.game_setup.player import Player
from interface.console import console_ui
from core.classes.moves import moves


class ConsoleGame:

    # def __init__(self):
    @staticmethod
    def request_players_info():
        # welcome both players to the romeo and juliet game
        console_ui.game_welcome()

        # ask for the players to enter their names
        player1_name = console_ui.ask_for_player_name(1)
        player2_name = console_ui.ask_for_player_name(2)

        # create the players
        player1 = Player(player1_name, 1)
        player2 = Player(player2_name, 2)

        console_ui.add_line_break()

        # welcome the players
        console_ui.welcome_players(player1_name, player2_name)
        pass

    def arrange_cards(self):
        pass

    def check_move(self, player, card):
        # Validate player's move
        pass

    def make_move(self, player, card):
        # Validate player's move
        pass

    @staticmethod
    def play():
        # welcome both players to the romeo and juliet game
        console_ui.game_welcome()

        # ask for the players to enter their names
        player1_name = console_ui.ask_for_player_name(1)
        player2_name = console_ui.ask_for_player_name(2)

        # create the players
        player1 = Player(player1_name, 1)
        player2 = Player(player2_name, 2)

        console_ui.add_line_break()

        # welcome the players
        console_ui.welcome_players(player1_name, player2_name)

        # create the pack of cards to be used for the gameplay
        console_ui.display_message('Creating the game...')
        # create the packs of card to be used
        card_pack = Pack()

        # display a message to the users that the game is being setup
        console_ui.display_message('Shuffling the pack...')
        # shuffle the card pack
        card_pack.shuffle_pack()

        # display a message to the users that the game is being setup
        console_ui.display_message('Arranging the cards...')
        # create the board for the game
        board = Board(card_pack)

        console_ui.add_line_break()

        # display the initial board
        board.display_board(player1.xPosition, player1.yPosition, player2.xPosition, player2.yPosition)

        # player moves

        # check player move

        # rinse and repeat
        moves.check_knight_move(0, 0)
