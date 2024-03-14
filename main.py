from game_play.console_game import ConsoleGame
from game_play.gui_game import GUIGame
from interface.console import console_ui
from core.classes.game_setup.board import Board
from core.classes.game_setup.pack import Pack


# def main():
#     # welcome both players to the romeo and juliet game
#     console_ui.game_welcome()
#
#     # create the pack of cards to be used for the gameplay
#     console_ui.display_message('Creating the game...')
#     # create the packs of card to be used
#     card_pack = Pack()
#
#     # display a message to the users that the game is being setup
#     console_ui.display_message('Shuffling the pack...')
#     # shuffle the card pack
#     card_pack.shuffle_pack()
#
#     # display a message to the users that the game is being setup
#     console_ui.display_message('Arranging the cards...')
#     # create the board for the game
#     board = Board(card_pack)
#
#     # play the console game
#     # next sprint will account for asking users which kind they want to play
#     console_game = ConsoleGame(board)
#     console_game.play_game()

def main():
    # welcome both players to the romeo and juliet game
    # console_ui.game_welcome()

    # create the pack of cards to be used for the gameplay
    # console_ui.display_message('Creating the game...')
    # create the packs of card to be used
    card_pack = Pack()

    # display a message to the users that the game is being setup
    # console_ui.display_message('Shuffling the pack...')
    # shuffle the card pack
    card_pack.shuffle_pack()

    # display a message to the users that the game is being setup
    # console_ui.display_message('Arranging the cards...')
    # create the board for the game
    board = Board(card_pack)

    # play the console game
    # next sprint will account for asking users which kind they want to play
    # console_game = ConsoleGame(board)
    # console_game.play_game()
    gui_game = GUIGame(board)
    gui_game.play_game()


if __name__ == "__main__":
    main()
