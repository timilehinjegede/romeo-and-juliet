from core.classes.game_setup.board import Board
from core.classes.game_setup.game import Game
from core.classes.game_setup.pack import Pack
from core.classes.game_setup.player import Player
from interface.console import console_ui


class ConsoleGame:
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

        console_ui.add_line_break();

        # welcome the players
        console_ui.welcome_players(player1_name, player2_name)

        # create the game class to be used for the gameplay
        console_ui.display_setup_message('Creating the game...')
        game = Game()

        # display a message to the users that the game is being setup
        console_ui.display_setup_message('Shuffling the pack..')
        # shuffle the card pack
        game.shuffle_deck()

        # display a message to the users that the game is being setup
        console_ui.display_setup_message('Arranging the cards...')
        # deal the cards and set up the board
        game.deal_cards()

        # create the packs of card to be used
        card_pack = Pack()

        # create the board for the game
        board = Board(card_pack)

        # display the initial board
        board.display_board(player1.xPosition, player1.yPosition, player2.xPosition, player2.yPosition)