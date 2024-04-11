from game_play.console_game import ConsoleGame
from game_play.gui_game import GUIGame
from interface.console import console_ui
from core.classes.game_setup.board import Board
from core.classes.game_setup.pack import Pack

def main():
    # create the packs of card to be used
    card_pack = Pack()

    # shuffle the card pack
    card_pack.shuffle_pack()

    # create the board for the game
    board = Board(card_pack)

    # play the GUI game
    gui_game = GUIGame(board)
    gui_game.play_game()


if __name__ == "__main__":
    main()
